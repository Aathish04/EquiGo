import requests

headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
}

data = '{"user": "user", "query": "I need to travel from my home to Adyar quickly, and Im in a wheelchair."}'

response = requests.post(' http://localhost:6001/', headers=headers, data=data)

print(response.json())