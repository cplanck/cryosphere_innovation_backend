import csv
import json
import os
from cmath import nan
from datetime import datetime
from operator import add

import requests

"""
This script migrates 'watched instruments' from the old system to the new system.
The old system was centered around the SIMB3 model, where the new system is centered 
around the deployment model. This script converts watched instruments to the respective 
deployments in the new system and updates the user profile. 

Note: this will probably give an error if ran in the future when new users have created
accounts on the old system that haven't gotten moved to the new system. It also assumes
that user_ids in the new system == user_ids in the old system. 
"""


def update_userprofile_with_watched_deployments(user, deployments):
    url = 'http://localhost:8000/users/profile/dashboard/watched_deployments/' + \
        str(user) + '/'
    payload = {'watched_deployments': deployments}
    print(payload)
    add_dashboard_deployments = requests.patch(url, data=payload)
    print(json.loads(add_dashboard_deployments.content))


# Map each IMEI into a deployment_id in the new system
deployment_ids = {}
deployments = json.loads(requests.get(
    'http://localhost:8000/api/internal/deployments').content)['results']

map_imei_to_id = {}
for deployment in deployments:
    map_imei_to_id[deployment['instrument']
                   ['serial_number']] = deployment['id']


# Get entire list of WatchedSIMB3s from old system
r = requests.get('http://localhost:8001/api/watched_simb3s')
watched_simb3s_list = json.loads(r.content)

# Get user SIMB3s organized in a dictionary as user_id: [imei_1, imei_2, ...]
watched_simb3s_by_user = {}
for simb3 in watched_simb3s_list:
    for user in simb3['simb3_users']:
        if user not in watched_simb3s_by_user:
            watched_simb3s_by_user[user] = [
                map_imei_to_id[str(simb3['simb3'])]]
        else:
            watched_simb3s_by_user[user].append(
                map_imei_to_id[str(simb3['simb3'])])

for user in watched_simb3s_by_user.keys():
    update_userprofile_with_watched_deployments(
        user, watched_simb3s_by_user[user])
