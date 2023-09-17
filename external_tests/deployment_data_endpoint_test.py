import requests
url = 'http://localhost:8000/public/deployment/data/e11478e8-8bda-4494-a796-08b82334dfa0/?field=dtc_values_158'; 
response = requests.get(url, headers={'Authorization':'Bearer 2OJ23lZpUUFKO80IC2v4mhp8gsASPbzV'}).json()
print(response)