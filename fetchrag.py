

import requests

r = requests.get("http://192.168.82.1:8000/fetchrag")


with open("/Users/aathishs/Projects/AIML/EquiGo/llm/data/pathway-docs-small/documents.jsonl","w") as f:
    f.write(r.json())