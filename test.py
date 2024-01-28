import requests
from urllib.parse import urlparse
headers = {
    'accept': 'application/json',
    # 'content-type': 'application/x-www-form-urlencoded',
}

data = '{"pref_lan":"ta","isaudio":false,"data":"நான் அடையாறிலிருந்து மைலாப்பூர் வரை பயணிக்க விரும்புகிறேன்."}'.encode("utf-8")
import json
json.loads(data)
response = requests.post('http://127.0.0.1:8000/planroute', headers=headers, data=data)

print(response.text)