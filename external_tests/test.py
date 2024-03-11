import requests


import requests
url = 'http://localhost:8000/public/deployments/9eed4974-a45b-4670-b807-a1e919543bb0'; 
response = requests.get(url, headers={'Authorization':'Bearer n6cQZOsEAzBN2NzN3m1regQXAFp2QUoA'}).json()
print(response)