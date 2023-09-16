import lambdaFunctions
import json
import boto3
import openai
import pymongo

client = boto3.client('textract', region_name='ap-south-1', aws_access_key_id='AKIA2NIZNTIRYKN4Y26M',
                     aws_secret_access_key='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' )

with open('/Users/pradxn/Desktop/BloodOCR/reportImages/Page1.jpg', 'rb') as image:
    img = bytearray(image.read())

response = client.detect_document_text(
    Document = {'Bytes' : img}
)

print(response)
print('\n')
