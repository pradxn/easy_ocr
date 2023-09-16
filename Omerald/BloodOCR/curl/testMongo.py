import pymongo
from bson import ObjectId
#from prettytable import PrettyTable
from tabulate import tabulate

myclient = pymongo.MongoClient('mongodb+srv://pradeepvajrala:M6dGJfkIZJVhPCZU@cluster0.qu3shkb.mongodb.net/')
db = myclient["test_database_name"]
collection = db["test_collection_name"]

keyInput = input('Document name: \n')
key = keyInput
#value = "NEUTROPHILS: 57.3%, LYMPHOCYTES: 30.2%, EOSINOPHILS: 3.5%, MONOCYTES: 7.4%, BASOPHILS: 1.6%, NEUTROPHILS: 2292 cells/cu.mm, LYMPHOCYTES: 1208 cells/cu.mm, EOSINOPHILS: 140 cells/cu.mm, MONOCYTES: 296 cells/cu.mm, BASOPHILS: 64 cells/cu.mm"
'''original_string = "NEUTROPHILS: 57.3%, LYMPHOCYTES: 30.2%, EOSINOPHILS: 3.5%, MONOCYTES: 7.4%, BASOPHILS: 1.6%, NEUTROPHILS: 2292 cells/cu.mm, LYMPHOCYTES: 1208 cells/cu.mm, EOSINOPHILS: 140 cells/cu.mm, MONOCYTES: 296 cells/cu.mm, BASOPHILS: 64 cells/cu.mm"
split_string = [f'"{s.strip()}"' for s in original_string.split(",")]
result_string = ", ".join(split_string)
value = result_string.split(", ")
print(value)
'''
original_string = "NEUTROPHILS: 57.3%, LYMPHOCYTES: 30.2%, EOSINOPHILS: 3.5%, MONOCYTES: 7.4%, BASOPHILS: 1.6%, NEUTROPHILS: 2292 cells/cu.mm, LYMPHOCYTES: 1208 cells/cu.mm, EOSINOPHILS: 140 cells/cu.mm, MONOCYTES: 296 cells/cu.mm, BASOPHILS: 64 cells/cu.mm"
split_string = [f'"{s.strip()}"' for s in original_string.split(",")]
result_string = ", ".join(split_string)
value = result_string.split(", ")

for i in range(len(value)):
    value[i] = value[i].strip('"')

print(value)

document = {key : value}
#print(document)
collection.insert_one(document)
object_id = str(document['_id'])
print("Save this id for future reference: "+ object_id)
print('\n')

object_id_str = input('Enter reference id: ')
#object_id = pymongo.ObjectId(object_id_str)
object_id = ObjectId(object_id_str)
document = collection.find_one({"_id": object_id})
#result = collection.find_one({'_id': object_id})

# Print the contents of the retrieved document
if document:
    value = document[key]
    print("{:<70}{}".format("Key", "Value"))
    for v in value:
        k, val = v.split(": ")
        print("{:<70}{}".format(k, val))
else:
    print("No document found with the given id.")

'''
if document:
    table = []
    for key, value in document.items():
        table.append([key, "\n".join(value)])
    print(tabulate(table, headers=["Key", "Value"], tablefmt="plain"))
else:
    print("No document found with the given id.")

if document:
    headers = ['Key', 'Value']
    rows = [[key, value] for key, value in document.items()]
    print(tabulate(rows, headers=headers, tablefmt='plain'))
else:
    print("No document found with the given id.")


if document:
    table = PrettyTable(['Value'])
    for key, value in document.items():
        table.add_row([value])
    print(table)
else:
    print("No document found with the given id.")


if document:
    for key, value in document.items():
        
        print(type(value))
        stringValue = str(value)
        print(stringValue)
else:
    print("No document found with the given id.")
'''


'''
NEUTROPHILS: 57.3%, LYMPHOCYTES: 30.2%, EOSINOPHILS: 3.5%
to "NEUTROPHILS: 57.3%", "LYMPHOCYTES: 30.2%", "EOSINOPHILS: 3.5%"
'''


#############################################################################################################################################################################################################################################################################################################################################
'''import pymongo

myclient = pymongo.MongoClient('mongodb+srv://pradeepvajrala:M6dGJfkIZJVhPCZU@cluster0.qu3shkb.mongodb.net/?retryWrites=true&w=majority', tls=True, tlsCAFile='/Users/pradxn/Desktop/BloodOCR/X509-cert-2196264278640773431.pem')
db = myclient["mydatabase"]
collection = db["customers"]


#key = input('Document name: ')
#value = "NEUTROPHILS: 57.3%, LYMPHOCYTES: 30.2%, EOSINOPHILS: 3.5%, MONOCYTES: 7.4%, BASOPHILS: 1.6%, NEUTROPHILS: 2292 Cells/cu.mm, LYMPHOCYTES: 1208 Cells/cu.mm, EOSINOPHILS: 140 Cells/cu.mm, MONOCYTES: 296 Cells/cu.mm, BASOPHILS: 64 Cells/cu.mm"
#responseJSON = { key : value }
#QuG19mCudHekBFmf
#responseJSON = { "name": "John", "address": "Highway 37" }
#result = collection.insert_one(responseJSON)
key = "Report"
value = "MCV: 12", "PCV: 14.6" #from openai prompt

document = {key : value}
collection.insert_one(document)
print(document)

dblist = myclient.list_database_names()
if "mydatabase" in dblist:
  print("The database exists.")

collist = mydb.list_collection_names()
if "customers" in collist:
  print("The collection exists.")

myclient.close()

'''



'''if document:
    for key in document:
        value = document[key]
        print("{:<15}{}".format(key, value))
        # Check if the value is a DLC
        if key == "DLC":
            for v in value.split(","):
                k, val = v.split(": ")
                print("{:<15}{}".format(k.strip(), val.strip()))
else:
    print("No document found with the given id.")
'''