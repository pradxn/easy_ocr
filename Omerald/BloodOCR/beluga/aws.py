'''
s3 = boto3.resource('s3')
bucket_name = 'omeraldreports-1'
object_key = 'Page1.jpg'

response = client.analyze_document(
    Document={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': object_key
        }
    },
    FeatureTypes=['TABLES', 'FORMS']
)
'''

import boto3
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
                temp_data["Name"] = value[0]
                temp_data["Result"] = value[1]
                temp_data["Units"] = value[2]
                temp_data["Ranges"] = value[3]
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

