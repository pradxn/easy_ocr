from flask import Flask, request, jsonify
import uuid
import boto3
import requests
import io
import json
import pymongo

app = Flask(__name__)

client = boto3.client('textract', region_name='ap-south-1', aws_access_key_id='AKIA2NIZNTIRYKN4Y26M',
                     aws_secret_access_key='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' )

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

myclient = pymongo.MongoClient('mongodb+srv://pradeepvajrala:M6dGJfkIZJVhPCZU@cluster0.kknndfq.mongodb.net/?retryWrites=true&w=majority')
db = myclient["Omerald_database"]
collection = db["Omerald_collection"]

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.get_json()
    image_url = data['image_url']
    file_name = data['file_name']
    file_name = data.get('file_name', '')

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

    raw_text = extract_text(response, extract_by="LINE")
    word_map = map_word_id(response)
    table = extract_table_info(response, word_map)
    key_map = get_key_map(response, word_map)
    value_map = get_value_map(response, word_map)
    final_map = get_kv_map(key_map, value_map)

    table_data = {key: values for key, values in table.items() if 'Test Description' in values[1][0]}
    json_data = generate_json(table_data)

    key = file_name or image_url

    document = {"key": key, "value": json_data}

    collection.insert_one(document)

    return jsonify({'success': True}), 200
