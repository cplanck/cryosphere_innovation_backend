import requests

staff_api_key = 'ltUhYcBWbhqk60JHLF6ExxjYSQXCW7YO'
regular_api_key = 'EwnrreO6UUsxFQUiwRXdn2ePWVnTiRTu'
bears_api_key = 'QBkOot5g7sxPg98ZVZ2JFXML9L4BByBl'

deployment_uuid = 'b3a08acc-b797-4e21-bf50-ab9d0dce244b'

data = [
    {'latitude': 83.321, 'longitude': 12.76, 'air_temp': 22.325, 'air_pressure': 2112, 'time_stamp': 1},
    {'latitude': 12.321, 'longitude': 45.76, 'air_temp': 34.325, 'air_pressure': 1013, 'time_stamp': 2},
    {'latitude': 43.321, 'longitude': 64.76, 'air_temp': 2.325, 'air_pressure': 1212, 'time_stamp': 3},
    {'latitude': 12.321, 'longitude': 34.76, 'air_temp': 9.325, 'air_pressure': 1212, 'time_stamp': 4}
]

# r = requests.get(f'http://localhost:8000/public/deployment/data/{deployment_uuid}', headers={'AUTHENTICATION':regular_api_key})
r = requests.patch(f'http://localhost:8000/public/deployment/data/{deployment_uuid}/', headers={'AUTHENTICATION':bears_api_key}, json=data)

print(r.json())

{'latitude': 83.321, 'longitude': 12.76, 'air_temp': 22.325, 'air_pressure': 1023}
