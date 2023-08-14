import os
from urllib import response

from bson import ObjectId
from dotenv import load_dotenv
from pymongo.errors import BulkWriteError
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

uri = 'mongodb+srv://' + os.environ['MONGO_USERNAME'] + ':' + os.environ['MONGO_PASSWORD'] + \
    '@cryosphere-innovation-m.enkpma5.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(uri, server_api=ServerApi('1'))
db = client['cryosphere-innovation-mongodb']


def mongo_collection_exists(collection_name):
    collection_names = db.list_collection_names()
    if collection_name in collection_names:
        return True
    else:
        return False


def create_mongodb_collection(collection_name, unique_index):
    """
    Create a MongoDB collection given a collection name and unique index.
    The unique index defines a attribute that is forced unique at the database level.
    """
    if not mongo_collection_exists(collection_name):
        collection = db.create_collection(collection_name)
        if unique_index:
            collection.create_index(unique_index, unique=True)

    else:
        return None

    if collection is not None:
        return collection_name
    else:
        return None


def delete_mongodb_collection(collection_name):
    """
    Delete a MongoDB collection given a collection name
    """
    collection = db[collection_name]

    if collection is not None:
        collection.drop()


def post_data_to_mongodb_collection(collection_name, data):
    collection = db[collection_name]
    try:
        collection.insert_many(data, ordered=False)
        return 'All documents added to collection' + collection_name
    except BulkWriteError as e:
        print(e)
        return "Documents with duplicate unique indexes found. " + str(e.details[' Inserted']) + ' documents inserted to ' + collection_name


def get_data_from_mongodb(collection_name, fields=None):
    collection = db[collection_name]

    response = []
    if fields:
        projection = {field_name: 1 for field_name in fields}
        projection['_id'] = 1
        documents = collection.find({}, projection).sort('time_stamp', 1)
    else:
        documents = collection.find(
            {}, {'_id': 1, 'uniqueID': 0}).sort('time_stamp', 1)

    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)

    return response

def delete_objects_from_mongo_db_collection_by_id(collection_name, object_id_array):
    collection = db[collection_name]
    formatted_object_ids = [ObjectId(oid) for oid in object_id_array]
    object_id_array.extend(formatted_object_ids)
    result = collection.delete_many({"_id": {"$in": object_id_array}})
    return result.deleted_count

def delete_all_data_from_mongodb_collection(collection_name):
    collection = db[collection_name]
    collection.delete_many({})
