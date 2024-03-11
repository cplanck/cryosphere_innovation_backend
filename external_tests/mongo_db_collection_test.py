import os
from urllib import response

from bson import ObjectId
from dotenv import load_dotenv
from pymongo.errors import BulkWriteError, DuplicateKeyError
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

uri = 'mongodb+srv://' + os.environ['MONGO_USERNAME'] + ':' + os.environ['MONGO_PASSWORD'] + \
    '@cryosphere-innovation-m.enkpma5.mongodb.net/?retryWrites=true&w=majority'


client = MongoClient(uri, server_api=ServerApi('1'))
db = client['cryosphere-innovation-mongodb']

# collection_name = '9eed4974-a45b-4670-b807-a1e919543bb0'
# collection = db[collection_name]

collection_names = ["9eed4974-a45b-4670-b807-a1e919543bb0", "01b01599-69ae-4685-9b0b-f83d57c9d74a"]  # Add more collection names here

# db = client.admin  # Connect to the admin database
# db.command("grantRolesToUser", os.environ['MONGO_USERNAME'], roles=["clusterMonitor"])


pipeline = [
    {"$currentOp": {}}  # Dummy stage to satisfy the requirement
]

for collection_name in collection_names:
    pipeline.append({
        "$unionWith": {
            "coll": collection_name,
            "pipeline": [
                {"$project": {"latitude": 1}}
            ]
        }
    })

cursor = db.aggregate(pipeline, allowDiskUse=True)

for document in cursor:
    print(document["latitude"])
