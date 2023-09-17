import requests
url = 'http://localhost:8000/public/deployment/data/e11478e8-8bda-4494-a796-08b82334dfa0'; 
response = requests.get(url, headers={'Authorization':'Bearer 4PnOu0TxcfNpr4ukDGXz5sAg4lOh1AjF'}).json()
print(response)