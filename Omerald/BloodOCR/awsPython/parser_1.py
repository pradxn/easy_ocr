import json
import uuid


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

print("...................................................................")

f = open('analyzeDocResponse.json')
response = json.load(f)

#print(json.dumps(response))

#raw_text = extract_text(response, extract_by="LINE")
word_map = map_word_id(response)
table = extract_table_info(response, word_map)
#key_map = get_key_map(response, word_map)
#value_map = get_value_map(response, word_map)
#final_map = get_kv_map(key_map, value_map)

#print(json.dumps(table))
#print(type(table))
#print(json.dumps(final_map))
#print(raw_text)
        
def print_table(data):
    for key, values in data.items():
        print("\n")
        for value in values:
            row = "|".join([str(x).ljust(20) for x in value])
            print(row)
                    
print_table(table)
#print(type(table))

print("...................................................................")
'''
test_name = input("Enter test name: ")

matching_row = None

for row in response:
    if isinstance(row, dict) and row.get('Test Name') == test_name:
        print(row)
        break  # exit loop after finding first matching row

if matching_row:
    print(matching_row)
else:
    print(f"No row found for test name '{test_name}'")

print("...................................................................")

row_to_extract = input("Enter the row to extract: ")
for table in response.values():
    for row in table:
        if row_to_extract in row[0]:
            test_description = row[0]
            result = row[1]
            units = row[2]
            reference_ranges = row[3]
            method = row[4]


print(f"Test Description: {test_description}")
print(f"Result: {result}")
print(f"Units: {units}")
print(f"Reference Ranges: {reference_ranges}")
print(f"Methods: {method}")

print("...................................................................")
'''
row_name = input("Enter test name: ")
#rowStr = "\"" + row_name + "\""

def extract_serum_data(table):
    req_tables = []
    for table_name, table in table.items():
        for row in table:
            if row_name in row[0]:
                req_tables.append(table)
    return req_tables
row = extract_serum_data(table)
'''
test_name = row[0][7][0]
result = row[0][7][1]
units = row[0][7][2]
bioRange = row[0][7][3]
method = row[0][7][4]
'''
#print(row)
print("\n")
#print(row[0])
print("\n")
for data in row[0]:
    if row_name.lower() in ' '.join(data).lower():
        print(data)
        test_name = data[0]
        result = data[1]
        units = data[2]
        bioRange = data[3]
        #method = data[4]
        print("\n")
        print(f"Test Description: {test_name}")
        print(f"Result: {result}")
        print(f"Units: {units}")
        print(f"Reference Ranges: {bioRange}")
        #print(f"Methods: {method}")
        

print("\n")

#convert into json data

'''
print(f"Test Description: {test_name}")
print(f"Result: {result}")
print(f"Units: {units}")
print(f"Reference Ranges: {bioRange}")
print(f"Methods: {method}")
print("\n")
print(row[0][7])
'''
print("\n")


'''
mcv_row = None
for rows in table:
    if rows[0] == 'MCV':
        mcv_row = rows
        break

if mcv_row is not None:
    print(mcv_row)
else:
    print("Row not found in data")
'''