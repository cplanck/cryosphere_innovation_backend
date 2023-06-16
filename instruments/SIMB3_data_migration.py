import json
import os
from cmath import nan
from datetime import datetime, timedelta

import requests
import xlrd
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

uri = 'mongodb+srv://' + os.environ['MONGO_USERNAME'] + ':' + os.environ['MONGO_PASSWORD'] + \
    '@cryosphere-innovation-m.enkpma5.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(uri, server_api=ServerApi('1'))
db = client['cryosphere-innovation-mongodb']


def delete_all_data_from_mongodb_collection(collection_name):
    collection = db[collection_name]
    collection.delete_many({})


def convert_time_stamp_to_unix(instrument_data):
    for item in instrument_data[0]:
        item['time_stamp'] = excel_to_unix(item['time_stamp'])
    return instrument_data[0]


def excel_to_unix(time_stamp):
    unix_timestamp = (time_stamp - 25569) * 86400
    return unix_timestamp


def update_deployment_data(imei):
    """
    Function for updating SIMB3 data in the MongoDB. Completely removes all 
    existing data and overwrites it with new data. 
    """

    instrument_data = requests.get(
        'http://www.cryosphereinnovation.com/api/simb3/query/?imei=' + str(imei)).json()

    # convert all time_stamps to UNIX
    instrument_data = convert_time_stamp_to_unix(instrument_data)

    # get data UUID in new system from the SIMB3 imei
    uuid = requests.get(
        'http://localhost:8000/api/internal/deployments/' + str(imei)).json()[0]['data_uuid']

    # delete all data in existing collection
    delete_all_data_from_mongodb_collection(uuid)

    # post request data to new system
    headers = {'Content-Type': 'application/json'}
    request = requests.post('http://localhost:8000/api/internal/modify/data/', headers=headers,
                            data=json.dumps({'data': instrument_data, 'deployment_uuid': uuid, 'primary_key': 'time_stamp'}))


imei = str(300434063382860)
imei = str(300434064563570)
imei = str(300434064560560)

deployments = requests.get(
    'http://localhost:8000/api/internal/deployments').json()

for deployment in deployments:

    # print(type(deployment['instrument']['serial_number']))

    print(deployment['data_uuid'])
    if (deployment['status'] == 'deployed'):
        print(deployment['instrument']['serial_number'])
        update_deployment_data(deployment['instrument']['serial_number'])
