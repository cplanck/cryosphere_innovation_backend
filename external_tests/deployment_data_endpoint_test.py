import requests
# url = 'http://localhost:8000/public/deployment/data/e11478e8-8bda-4494-a796-08b82334dfa0/?field=dtc_values_158'; 
# response = requests.get(url, headers={'Authorization':'Bearer 2OJ23lZpUUFKO80IC2v4mhp8gsASPbzV'}).json()
# print(response)


# url = 'http://localhost:8000/public/deployments/300434066157890'; 
# response = requests.get(url, headers={'Authorization':'Bearer QBkOot5g7sxPg98ZVZ2JFXML9L4BByBl'}).json()
# print(response)


import requests
url = 'http://localhost:8000/public/deployment/data/a298311f-3aec-44f6-8c5c-c82982b87c82'; 
response = requests.get(url, headers={'Authorization':'Bearer carnVbVqWLUQR2yvw075XuKhTzATz2J8'}).json()
print(len(response))