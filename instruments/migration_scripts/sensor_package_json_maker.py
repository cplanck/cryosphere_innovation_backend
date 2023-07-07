import json

import requests

data_sheet = requests.get(
    'http://localhost:8000/deployment/data/3a8ffb3a-2077-4f92-8e81-4c9f9eb7cfc8')

fields = data_sheet.json()[0]

json_list = []
count = 0
for field in fields:
    # print(field.split('_'))
    pretty_field_name = field
    if field.split('_')[0] == 'dtc':
        dtc_field_num = field.split('_')[2]
        pretty_field_name = 'Temperature String Sensor ' + dtc_field_num
    json_list.append({"id": count, "fieldName": field,
                     "name": pretty_field_name, "precision": 3})
    count = count + 1

print(json.dumps(json_list))
