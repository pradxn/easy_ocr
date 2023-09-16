'''import json
import uuid
import boto3

client = boto3.client('textract', region_name='ap-south-1', aws_access_key_id='AKIA2NIZNTIRYKN4Y26M',
                     aws_secret_access_key='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' )

s3 = boto3.resource('s3')
bucket_name = 'omeraldreports-1'
object_key = 'Page1.jpg'
s3_url = f"s3://omeraldreports-1/Page1.jpg"

response = client.start_document_text_detection(
    DocumentLocation={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': object_key
        }
    }
)

job_id = response['JobId']

while True:
    response = client.get_document_text_detection(JobId=job_id)
    status = response['JobStatus']
    if status == 'SUCCEEDED':
        break
    if status == 'FAILED':
        raise Exception('Text detection job failed')

blocks = response['Blocks']
lines = [block['Text'] for block in blocks if block['BlockType'] == 'LINE']
parsed_text = '\n'.join(lines)

#print(parsed_text)
#print(response)
print(type(response))

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

raw_text = extract_text(response, extract_by="LINE")
word_map = map_word_id(response)
table = extract_table_info(response, word_map)
key_map = get_key_map(response, word_map)
value_map = get_value_map(response, word_map)
final_map = get_kv_map(key_map, value_map)

def print_table(data):
    for key, values in data.items():
        print("\n")
        for value in values:
            row = "|".join([str(x).ljust(20) for x in value[0:4]])
            print(row)

print_table(table)'''

'''import json
import uuid
import boto3

client = boto3.client('textract', region_name='ap-south-1', aws_access_key_id='AKIA2NIZNTIRYKN4Y26M',
                     aws_secret_access_key='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' )

s3 = boto3.resource('s3')
bucket_name = 'omeraldreports-1'
object_key = 'Page1.jpg'
s3_url = f"s3://omeraldreports-1/Page1.jpg"

response = client.analyze_document(
    DocumentLocation={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': object_key
        }
    }
)

job_id = response['JobId']

while True:
    response = client.get_document_text_detection(JobId=job_id)
    status = response['JobStatus']
    if status == 'SUCCEEDED':
        break
    if status == 'FAILED':
        raise Exception('Text detection job failed')

blocks = response['Blocks']
lines = [block['Text'] for block in blocks if block['BlockType'] == 'LINE']
parsed_text = '\n'.join(lines)

# create a dictionary to store the code and other relevant information
data = {
    'code': response
}

# save the data to a JSON file
with open('data.json', 'w') as f:
    json.dump(data, f)
'''

'''import boto3
import requests
import io
import json
import lambdaFunctions
import pymongo

client = boto3.client('textract', region_name='ap-south-1', aws_access_key_id='AKIA2NIZNTIRYKN4Y26M',
                     aws_secret_access_key='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' )

image_url = 'https://omeraldreports-1.s3.ap-south-1.amazonaws.com/Page1.jpg'
image_binary = io.BytesIO(requests.get(image_url).content).getvalue()

response = client.analyze_document(
    Document={
        'Bytes': image_binary
    },
    FeatureTypes=['TABLES', 'FORMS']
)

blocks = response['Blocks']
lines = [block['Text'] for block in blocks if block['BlockType'] == 'LINE']
parsed_text = '\n'.join(lines)

#print(parsed_text)
#print(response)
print('\n')
print(type(response))
print('\n')

raw_text = lambdaFunctions.extract_text(response, extract_by="LINE")
word_map = lambdaFunctions.map_word_id(response)
table = lambdaFunctions.extract_table_info(response, word_map)
key_map = lambdaFunctions.get_key_map(response, word_map)
value_map = lambdaFunctions.get_value_map(response, word_map)
final_map = lambdaFunctions.get_kv_map(key_map, value_map)

def print_table(data):
    output = ""
    for key, values in data.items():
        if 'Test Description' in values[1]:
            output += "\n"
            for value in values:
                row = "|".join([str(x).ljust(20) for x in value[0:4]])
                output += row + "\n"
    return output
print('\n')

print_table(table)

#outParsed = print_table(table)
print('\n')
test_data = {key: values for key, values in table.items() if 'Test Description' in values[1][0]}
values_list = list(test_data.values())
outParsed = print(values_list)
print(values_list)
#print(table)

myclient = pymongo.MongoClient('mongodb+srv://pradeepvajrala:M6dGJfkIZJVhPCZU@cluster0.qu3shkb.mongodb.net/')
db = myclient["Omerald_database"]
collection = db["Omerald_collection"]

try:
    myclient.admin.command('ping')
    print('\n')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    print('\n')
except Exception as e:
    print('\n')
    print(e)
    print('\n')

keyInput = input('Document name: ')

key = keyInput
original_string = outParsed

split_string = [f'"{s.strip()}"' for s in original_string.split(",")]
result_string = ", ".join(split_string)
value = result_string.split(", ")

for i in range(len(value)):
    value[i] = value[i].strip('"')

document = {key : value}
print('\n')
print(document)
print('\n')
collection.insert_one(document)
'''

'''import boto3
import requests
import io
import json
import lambdaFunctions
import pymongo

client = boto3.client('textract', region_name='ap-south-1', aws_access_key_id='AKIA2NIZNTIRYKN4Y26M',
                     aws_secret_access_key='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' )

image_url = 'https://omeraldreports-1.s3.ap-south-1.amazonaws.com/Page2.jpg'
image_binary = io.BytesIO(requests.get(image_url).content).getvalue()

response = client.analyze_document(
    Document={
        'Bytes': image_binary
    },
    FeatureTypes=['TABLES', 'FORMS']
)

blocks = response['Blocks']
lines = [block['Text'] for block in blocks if block['BlockType'] == 'LINE']
parsed_text = '\n'.join(lines)

#print(parsed_text)
#print(response)
print('\n')
print(type(response))

raw_text = lambdaFunctions.extract_text(response, extract_by="LINE")
word_map = lambdaFunctions.map_word_id(response)
table = lambdaFunctions.extract_table_info(response, word_map)
key_map = lambdaFunctions.get_key_map(response, word_map)
value_map = lambdaFunctions.get_value_map(response, word_map)
final_map = lambdaFunctions.get_kv_map(key_map, value_map)

def print_table(data):
    for key, values in data.items():
        if 'Test Description' in values[1]:
            print("\n")
            for value in values:
                row = "|".join([str(x).ljust(20) for x in value[0:4]])
                #print(row)
                return row

print('\n')

print(table)
#print_table(table)
print('\n')

test_data = {key: values for key, values in table.items() if 'Test Description' in values[1][0]}
values_list = list(test_data.values())
print(values_list)
outParsed = values_list
#print(table)

myclient = pymongo.MongoClient('mongodb+srv://pradeepvajrala:M6dGJfkIZJVhPCZU@cluster0.kknndfq.mongodb.net/?retryWrites=true&w=majority')
db = myclient["Omerald_database"]
collection = db["Omerald_collection"]

try:
    myclient.admin.command('ping')
    print('\n')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    print('\n')
except Exception as e:
    print('\n')
    print(e)
    print('\n')

keyInput = input('Document name: ')

if keyInput:
    key = keyInput
    original_string = outParsed

    value = original_string

    document = {"key": key, "value": value}

    collection.insert_one(document)
    print('\n')
    print("Data successfully inserted into MongoDB!")
    print('\n')

    '''

'''import boto3
import requests
import io
import json
import lambdaFunctions
import pymongo

client = boto3.client('textract', region_name='ap-south-1', aws_access_key_id='AKIA2NIZNTIRYKN4Y26M',
                     aws_secret_access_key='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' )

image_url = 'https://omeraldreports-1.s3.ap-south-1.amazonaws.com/Complete+Blood+Count+(CBC).pdf'
image_binary = io.BytesIO(requests.get(image_url).content).getvalue()

response = client.analyze_document(
    Document={
        'Bytes': image_binary
    },
    FeatureTypes=['TABLES', 'FORMS']
)

blocks = response['Blocks']
lines = [block['Text'] for block in blocks if block['BlockType'] == 'LINE']
parsed_text = '\n'.join(lines)

raw_text = lambdaFunctions.extract_text(response, extract_by="LINE")
word_map = lambdaFunctions.map_word_id(response)
table = lambdaFunctions.extract_table_info(response, word_map)
key_map = lambdaFunctions.get_key_map(response, word_map)
value_map = lambdaFunctions.get_value_map(response, word_map)
final_map = lambdaFunctions.get_kv_map(key_map, value_map)

def generate_json(table_data):
    json_data = []
    for key, values in table_data.items():
        if 'Test Description' in values[1][0]:
            temp_data = {}
            for value in values:
                temp_data[value[0]] = value[0:4]
            json_data.append(temp_data)
    return json_data

table_data = {key: values for key, values in table.items() if 'Test Description' in values[1][0]}
json_data = generate_json(table_data)
print(json_data)

myclient = pymongo.MongoClient('mongodb+srv://pradeepvajrala:M6dGJfkIZJVhPCZU@cluster0.kknndfq.mongodb.net/?retryWrites=true&w=majority')
db = myclient["Omerald_database"]
collection = db["Omerald_collection"]

try:
    myclient.admin.command('ping')
    print('\n')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    print('\n')
except Exception as e:
    print('\n')
    print(e)
    print('\n')

keyInput = input('Document name: ')

if keyInput:
    key = keyInput
    original_string = json_data

    value = original_string

    document = {"key": key, "value": value}

    collection.insert_one(document)
    print('\n')
    print("Data successfully inserted into MongoDB!")
    print('\n')
'''

import boto3
import requests
import io
import json
import pymongo

# AWS credentials
client = boto3.client('textract', region_name='ap-south-1', aws_access_key_id='AKIA2NIZNTIRYKN4Y26M',
                     aws_secret_access_key='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' )

# Read the image from URL and pass it to Textract
image_url = 'https://omeraldreports-1.s3.ap-south-1.amazonaws.com/Page2.jpg'
image_binary = io.BytesIO(requests.get(image_url).content).getvalue()

response = client.analyze_document(
    Document={
        'Bytes': image_binary
    },
    FeatureTypes=['TABLES', 'FORMS']
)

# Extract table information
blocks = response['Blocks']
table = {}
for block in blocks:
    if block['BlockType'] == 'TABLE':
        for index, cell in enumerate(block['Relationships'][0]['Ids']):
            if cell in table:
                table[cell].append(block['Blocks'][index]['Text'])
            else:
                table[cell] = [block['Blocks'][index]['Text']]
table_data = {}
for key in table:
    table_data[table[key][0]] = table[key][1:]

# Extract required data from table
output_data = {}
for key, values in table_data.items():
    if key == 'Hemoglobin':
        output_data['Name'] = key
        output_data['Result'] = values[0]
        output_data['Units'] = values[1]
        output_data['Ranges'] = values[2]

# Connect to MongoDB
myclient = pymongo.MongoClient('mongodb+srv://pradeepvajrala:M6dGJfkIZJVhPCZU@cluster0.kknndfq.mongodb.net/?retryWrites=true&w=majority')
db = myclient["Omerald_database"]
collection = db["Omerald_collection"]

# Insert data into MongoDB
document = {"Name": output_data['Name'], "Result": output_data['Result'], "Units": output_data['Units'], "Ranges": output_data['Ranges']}
collection.insert_one(document)
print("Data successfully inserted into MongoDB!")
