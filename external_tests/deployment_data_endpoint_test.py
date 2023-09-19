import requests
# url = 'http://localhost:8000/public/deployment/data/e11478e8-8bda-4494-a796-08b82334dfa0/?field=dtc_values_158'; 
# response = requests.get(url, headers={'Authorization':'Bearer 2OJ23lZpUUFKO80IC2v4mhp8gsASPbzV'}).json()
# print(response)


url = 'https://api.cryospherex.com/public/deployments/300434066157890'; 
response = requests.get(url, headers={'Authorization':'Bearer QBkOot5g7sxPg98ZVZ2JFXML9L4BByBl'}).json()
print(response)
