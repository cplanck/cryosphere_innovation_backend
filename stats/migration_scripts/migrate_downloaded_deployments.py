import requests
import json

url = 'http://localhost:8000/stats/deployment-download/'

with open('downloaded_simb3s.json', 'r') as json_file:
    json_data = json.load(json_file)

def get_deployment_pk(imei):
    r = requests.get('http://localhost:8000/deployments/' + str(imei)).json()
    return r['id']

for item in json_data:
    imei = item['fields']['simb3']
    try:
        id = get_deployment_pk(imei)

        users = item['fields']['simb3_users']
        for user in users:
            payload = {'deployment': id, 'user': user}
            r = requests.post(url, json=payload)
            print(r.content)
    except:
        print('Unabled to post for ' + str(imei))
