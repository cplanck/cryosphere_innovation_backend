import requests


# import requests
# url = 'http://localhost:8000/public/deployments/300434066157890'; 
# response = requests.get(url, headers={'Authorization':'Bearer carnVbVqWLUQR2yvw075XuKhTzATz2J8'}).json()
# print(response)

# import requests
# url = 'http://localhost:8000/public/deployment/data/e11478e8-8bda-4494-a796-08b82334dfa0'; 
# response = requests.get(url, headers={'Authorization':'Bearer carnVbVqWLUQR2yvw075XuKhTzATz2J8'}).json()
# print(response)

import requests
url = 'http://localhost:8000/public/deployments/300434063377240'; 
response = requests.get(url, headers={'Authorization':'Bearer n6cQZOsEAzBN2NzN3m1regQXAFp2QUoA'}).json()
print(response)