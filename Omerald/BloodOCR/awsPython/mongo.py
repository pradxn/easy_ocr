import pymongo
from bson.objectid import ObjectId

#db = pymongo.MongoClient('mongodb+srv://pradeep:zmkoxDl2NEoPCPFT@cluster1.fewx6mu.mongodb.net/?retryWrites=true&w=majority')

client = pymongo.MongoClient('mongodb+srv://pradeep:zmkoxDl2NEoPCPFT@cluster1.fewx6mu.mongodb.net/?retryWrites=true&w=majority')
db = client["test_database_name"]

collection = db["test_collection_name"]
key = "Test Reports Data"
#value = "Apple = 12", "Banana = 13.6 mg/L"
value = "PCV = 37.70 %", "HB = 12.2 g/dL", "CRP = 18.605 mg/L", "Hematocrit = 37.70%", "MCV = 87fL", "HB: 12.2g/dL", "DLC: Neutrophils: 57.3%, Lymphocytes: 30.2%, Eosinophils: 3.5%, Monocytes: 7.4%, Basophils: 1.6%"
#value = "PCV = 37.70 %", "HB = 12.2 g/dL", "CRP = 18.605 mg/L"
document = {key : value}
collection.insert_one(document)
#print(document)
object_id = str(document['_id'])
print("Save this id for future reference: "+ object_id)
print('\n')
object_id_str = input('Enter reference id: ')
#'64350c6c761ebe7924c382a4'
# convert the object id string to ObjectId type
object_id = ObjectId(object_id_str)

# retrieve the document with the given object id
document = collection.find_one({'_id': object_id})

# print the retrieved document
print(document[key])
client.close()