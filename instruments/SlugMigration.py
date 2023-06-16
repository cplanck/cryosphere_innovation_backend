import json
import os
from cmath import nan
from datetime import datetime

import requests
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()


deployments = requests.get(
    'http://localhost:8000/api/internal/deployments/').json()
headers = {'Content-Type': 'application/json'}


for deployment in deployments['results']:
    imei = deployment['instrument']['serial_number']
    request = requests.patch(
        'http://localhost:8000/api/internal/deployments/' + imei + '/', headers=headers, data=json.dumps({'slug': 'simb3/' + str(imei)}))


# print(deployments)
