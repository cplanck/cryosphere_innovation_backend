import requests
url = 'http://localhost:8000/public/deployment/data/9eed4974-a45b-4670-b807-a1e919543bb0'; 
response = requests.get(url, headers={'Authorization':'Bearer carnVbVqWLUQR2yvw075XuKhTzATz2J8'}).json()
print(response)