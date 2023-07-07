"""
This is the a script for porting SIMB3s from the old Cryosphere system
to the new deployment-centered system. 
"""

import json
from cmath import nan
from datetime import datetime

import requests

# def create_instrument(simb3):
#     if simb3['status'] == 'Active':
#         status = 1
#     elif simb3['status'] == 'Retired':
#         status = 0
#     elif simb3['status'] == 'Awaiting Deployment':
#         status = 2
#     elif simb3['status'] == 'Testing':
#         status = 3

#     instrument = {
#         'name': simb3['name'],
#         'status': status,
#         'serial_number': simb3['imei'],
#         'instrument_type': 'SIMB3'
#     }

#     headers = {
#         'Content-Type': 'application/json'  # Set the content type to JSON
#     }

#     request = requests.(
#         'http://localhost:8000/api/internal/simb3_instrument_migration/', headers=headers, data=json.dumps(instrupostment))

#     print(request)


def convert_date_8601(date_string):
    if date_string:
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        date_8061 = date_object.strftime("%Y-%m-%dT%H:%M:%S")
        print(date_8061)
        return str(date_8061)
    else:
        return None


def get_deployment_details(simb3):
    if simb3['status'] == 'Active':
        status = 1
    elif simb3['status'] == 'Retired':
        status = 0
    elif simb3['status'] == 'Awaiting Deployment':
        status = 2
    elif simb3['status'] == 'Testing':
        status = 3

    mb_plot_parameters = simb3['mb_plot_parameters'].split(',')

    details = {
        'sensor_suite': simb3['sensor_suite'],
        'version': simb3['version'],
        'fetch_data': simb3['fetch_data'],
        'decode': simb3['decode'],
        'post_to_database': simb3['post_to_database'],
        'deployment_ice_thickness': simb3['deployment_ice_thickness'],
        'deployment_snow_thickness': simb3['deployment_snow_thickness'],
        'starting_row': simb3['starting_row'],
        'ending_row': simb3['ending_row'],
        'mb_plot_parameters': {
            'surface_remove_above': mb_plot_parameters[0],
            'surface_remove_below': mb_plot_parameters[1],
            'surface_linear_shift': mb_plot_parameters[2],
            'bottom_remove_above': mb_plot_parameters[3],
            'bottom_remove_below': mb_plot_parameters[4],
            'bottom_linear_shift': mb_plot_parameters[5]
        },
        'transmission_interval': simb3['transmission_interval'],
        'funding_source': simb3['funding_source'],


    }
    data = {
        'status': status,
        'deployment_start_date': convert_date_8601(simb3['deployed_date']),
        'deployment_end_date': convert_date_8601(simb3['recovered_date']),
        'notes': simb3['deployment_notes'],
        'location': simb3['location'],
        'details': details
    }

    return data


new_simb3s = requests.get(
    'http://localhost:8000/api/internal/instruments').json()['results']

for simb3 in new_simb3s:
    imei = simb3['serial_number']
    instrument_id = simb3['id']
    old_simb3 = requests.get(
        'http://www.cryosphereinnovation.com/api/simb3/meta/?imei=' + imei).json()

    details = get_deployment_details(old_simb3[0])

    headers = {
        'Content-Type': 'application/json'
    }

    url = 'http://localhost:8000/api/internal/simb3_deployment_migration/' + \
        str(instrument_id) + '/'
    print(details)
    requests.patch(url, headers=headers, data=json.dumps(details))


# deployment_details = get_deployment_details(request[0])


# url = 'http://localhost:8000/api/internal/simb3_deployment_migration/' + \
#     str(request[0]['id']) + '/'

# requests.patch(
#     url, headers=headers, data=json.dumps(deployment_details))


# pseudocode:
    # get list of instruments in new system
    # for each serial_number, make a request to old endpoint
    # take response and use it to build deployment_details
    # PATCH this response to the deployment endpoint using the instrument_id
    # get simb3 metadata from old endpoint
    # get instrument_id of simb3 in new system
    # PATCH deployment details using id from new system
