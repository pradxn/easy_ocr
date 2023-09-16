import uuid
import json
import openai
import pymongo
from bson import ObjectId
#from prettytable import PrettyTable
from tabulate import tabulate

#code for parsing JSON based on type of word data
def extract_text(response, extract_by="WORD"):
    line_text = []
    for block in response["Blocks"]:
        if block["BlockType"] == extract_by:
            line_text.append(block["Text"])
    return line_text


def map_word_id(response):
    word_map = {}
    for block in response["Blocks"]:
        if block["BlockType"] == "WORD":
            word_map[block["Id"]] = block["Text"]
        if block["BlockType"] == "SELECTION_ELEMENT":
            word_map[block["Id"]] = block["SelectionStatus"]
    return word_map


def extract_table_info(response, word_map):
    row = []
    table = {}
    ri = 0
    flag = False

    for block in response["Blocks"]:
        if block["BlockType"] == "TABLE":
            key = f"table_{uuid.uuid4().hex}"
            table_n = +1
            temp_table = []

        if block["BlockType"] == "CELL":
            if block["RowIndex"] != ri:
                flag = True
                row = []
                ri = block["RowIndex"]

            if "Relationships" in block:
                for relation in block["Relationships"]:
                    if relation["Type"] == "CHILD":
                        row.append(" ".join([word_map[i] for i in relation["Ids"]]))
            else:
                row.append(" ")

            if flag:
                temp_table.append(row)
                table[key] = temp_table
                flag = False
    return table


def get_key_map(response, word_map):
    key_map = {}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET" and "KEY" in block["EntityTypes"]:
            for relation in block["Relationships"]:
                if relation["Type"] == "VALUE":
                    value_id = relation["Ids"]
                if relation["Type"] == "CHILD":
                    v = " ".join([word_map[i] for i in relation["Ids"]])
                    key_map[v] = value_id
    return key_map


def get_value_map(response, word_map):
    value_map = {}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET" and "VALUE" in block["EntityTypes"]:
            if "Relationships" in block:
                for relation in block["Relationships"]:
                    if relation["Type"] == "CHILD":
                        v = " ".join([word_map[i] for i in relation["Ids"]])
                        value_map[block["Id"]] = v
            else:
                value_map[block["Id"]] = "VALUE_NOT_FOUND"

    return value_map


def get_kv_map(key_map, value_map):
    final_map = {}
    for i, j in key_map.items():
        final_map[i] = "".join(["".join(value_map[k]) for k in j])
    return final_map
#######################################################################################################################################

print('\n')
f = open('analyzeDocResponse.json')
response = json.load(f)
print(type(response))

raw_text = extract_text(response, extract_by="LINE")
word_map = map_word_id(response)
table = extract_table_info(response, word_map)
key_map = get_key_map(response, word_map)
value_map = get_value_map(response, word_map)
final_map = get_kv_map(key_map, value_map)

#print(type(table))
#######################################################################################################################################
print(raw_text)
#prints table data in table format
def print_table(data):
    for key, values in data.items():
        print("\n")
        for value in values:
            row = "|".join([str(x).ljust(20) for x in value[0:4]])
            print(row)

print_table(table)

strTable = str(table)
print("####################################################################################")
print('\n')
row_name = input("Enter tests names (in CAPS): ")
rowStr = str(row_name)
print('\n')

openai.api_key = open("key.txt", "r").read().strip('\n')
def dataParsed(params):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = "Values of " + params + " from " + strTable + ":, comma and line separated",
        #prompt = "What are the values of " + params + " in " + strX,
        #prompt="Values of " + params + " in " + strX,
        temperature=0.7,
        max_tokens=2048
    )
    #total_response = response
    selected_response = response.choices[0].text.strip()
    return selected_response
    #return total_response

outputParsed = dataParsed(rowStr)
print(outputParsed)
print('\n')
#print(type(outputParsed))
'''
def extract_data(table):
    req_tables = []
    for table_name, table in table.items():
        for row in table:
            if row_name in row[0]:
                req_tables.append(table)
    return req_tables
row = extract_data(table)

print("\n")
print("\n")

for data in row[0]:
    if row_name.lower() in ' '.join(data).lower():
        print(data)
        test_name = data[0]
        result = data[1]
        #units = data[2]
        #bioRange = data[3]
        #method = data[4]
        print("\n")
        print(f"Test Description: {test_name}")
        print(f"Result: {result}")
        #print(f"Units: {units}")
        #print(f"Reference Ranges: {bioRange}")
        #print(f"Methods: {method}")

print("\n")
print("\n")
'''
#######################################################################################################################################

myclient = pymongo.MongoClient('mongodb+srv://pradeepvajrala:M6dGJfkIZJVhPCZU@cluster0.qu3shkb.mongodb.net/')
db = myclient["Omerald_database"]
collection = db["Omerald_collection"]

keyInput = input('Document name: ')
print('\n')
key = keyInput
original_string = outputParsed
#original_string = "NEUTROPHILS: 57.3%, LYMPHOCYTES: 30.2%, EOSINOPHILS: 3.5%, MONOCYTES: 7.4%, BASOPHILS: 1.6%, NEUTROPHILS: 2292 cells/cu.mm, LYMPHOCYTES: 1208 cells/cu.mm, EOSINOPHILS: 140 cells/cu.mm, MONOCYTES: 296 cells/cu.mm, BASOPHILS: 64 cells/cu.mm"
split_string = [f'"{s.strip()}"' for s in original_string.split(",")]
result_string = ", ".join(split_string)
value = result_string.split(", ")

for i in range(len(value)):
    value[i] = value[i].strip('"')

#print(value)

document = {key : value}
#print(document)
collection.insert_one(document)
object_id = str(document['_id'])
print("Save this id for future reference: "+ object_id)
print('\n')

object_id_str = input('Enter reference id: ')
print('\n')
#object_id = pymongo.ObjectId(object_id_str)
object_id = ObjectId(object_id_str)
document = collection.find_one({"_id": object_id})
#result = collection.find_one({'_id': object_id})

# Print the contents of the retrieved document

#document = {"TLC": "4000 cells/cu.mm", "MCV": "87 fL", "DLC": "Neutrophils: 57.3%, Lymphocytes: 30.2%, Eosinophils: 3.5%, Monocytes: 7.4%, Basophils: 1.6%"}

if document:
    value = document[key]
    print("{:<15}{}".format("Key", "Value"))
    print('--------------------')
    if isinstance(value, str):
        print("{:<15}{}".format(key, value))
        print('\n')
    else:
        for v in value:
            if ":" in v:
                k, val = v.split(": ")
                print("{:<15}{}".format(k, val))
            else:
                print("{:<15}{}".format(key, v))
                print('\n')
else:
    print("No document found with the given id.")

print('\n')
#######################################################################################################################################
