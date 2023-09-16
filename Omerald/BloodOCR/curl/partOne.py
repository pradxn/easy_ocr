'''
this part contains code that takes JSON input
and parses it for TABLE DATA
from which OPENAI takes the input params and returns required values
'''

import uuid
import json
import openai
import pymongo



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

#print(json.dumps(response))

#raw_text = extract_text(response, extract_by="LINE")
word_map = map_word_id(response)
table = extract_table_info(response, word_map)
#key_map = get_key_map(response, word_map)
#value_map = get_value_map(response, word_map)
#final_map = get_kv_map(key_map, value_map)

#print(table)
#print(json.dumps(table))
#print(type(table))
#print(json.dumps(final_map))
#print(raw_text)
#######################################################################################################################################

#keys are table names: table_82dce734e39f487ea33eb19adfa53dbf
#values are the required data

#prints table data in table format
def print_table(data):
    for key, values in data.items():
        print("\n")
        for value in values:
            row = "|".join([str(x).ljust(20) for x in value[0:2]])
            print(row)

print_table(table)

strTable = str(table)
print("#######################################################################################################################################")
print('\n')
row_name = input("Enter test name: ")
rowStr = str(row_name)
print('\n')

openai.api_key = open("key.txt", "r").read().strip('\n')
def dataParsed(params):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = "Values of " + params + " from " + strTable + " comma and line separated",
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

def extract_data(table):
    req_tables = []
    for table_name, table in table.items():
        for row in table:
            if row_name in row[0]:
                req_tables.append(table)
    return req_tables
row = extract_data(table)

#print(row[0])
#this only prints data which we give in input "test name"

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
#######################################################################################################################################
'''client = pymongo.MongoClient('mongodb+srv://pradeep:zmkoxDl2NEoPCPFT@cluster1.fewx6mu.mongodb.net/?retryWrites=true&w=majority')
db = client["OpenAI_database_name"]
collection = db["OpenAI_collection_name"]

keyInput = input('Document name: \n')
key = keyInput
value = output #from openai prompt

document = {key : value}
collection.insert_one(document)
object_id = str(document['_id'])
print("Save this id for future reference: "+ object_id)
print('\n')

object_id_str = input('Enter reference id: ')
object_id = ObjectId(object_id_str)
# retrieve the document with the given object id
document = collection.find_one({'_id': object_id})

# print the retrieved document
print(document)
print('\n')
print(document[key])
client.close()
'''
'''
client = pymongo.MongoClient('mongodb+srv://pradeep:zmkoxDl2NEoPCPFT@cluster1.fewx6mu.mongodb.net/?retryWrites=true&w=majority')
db = client["OpenAI_database_name"]
collection = db["OpenAI_collection_name"]
keyInput = input('Document name: \n')
key = keyInput
output = outputParsed
value = output
document = {key : value}
collection.insert_one(document)
print(document)
'''
'''
object_id = str(document['_id'])
print("Save this id for future reference: "+ object_id)
print('\n')
object_id_str = input('Enter reference id: ')

object_id = bson.objectid.ObjectId(object_id_str)
# retrieve the document with the given object id
document = collection.find_one({'_id': object_id})
print(document[key])

client.close()
'''
'''
myclient = pymongo.MongoClient('mongodb+srv://pradeep:zmkoxDl2NEoPCPFT@cluster1.fewx6mu.mongodb.net/?retryWrites=true&w=majority')
db = myclient["mydatabase"]
collection = db["customers"]


#key = input('Document name: ')
#value = "NEUTROPHILS: 57.3%, LYMPHOCYTES: 30.2%, EOSINOPHILS: 3.5%, MONOCYTES: 7.4%, BASOPHILS: 1.6%, NEUTROPHILS: 2292 Cells/cu.mm, LYMPHOCYTES: 1208 Cells/cu.mm, EOSINOPHILS: 140 Cells/cu.mm, MONOCYTES: 296 Cells/cu.mm, BASOPHILS: 64 Cells/cu.mm"
#responseJSON = { key : value }
responseJSON = { "name": "John", "address": "Highway 37" }
result = collection.insert_one(responseJSON)
print(result)

dblist = myclient.list_database_names()
if "mydatabase" in dblist:
  print("The database exists.")

collist = mydb.list_collection_names()
if "customers" in collist:
  print("The collection exists.")

myclient.close()
'''