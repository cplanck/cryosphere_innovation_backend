import json

import requests

backend_root = 'https://api.citestingx.com/api/internal/deployments/?status=deployed'
backend_root = 'http://localhost:8000/api/internal/deployments/?status=deployed'
headers = {'Authorization': 'ltUhYcBWbhqk60JHLF6ExxjYSQXCW7YO'}

deployed_deployments = requests.get(
    backend_root, headers=headers).json()['results']
