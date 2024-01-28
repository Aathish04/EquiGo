import json
import requests
from dotenv import load_dotenv
load_dotenv()
import os

def llmgetjson(iptext):
    text = iptext
    prompt = f"JSON of startlocation  endlocation  vehicletype  visionImpairment  mobilityPhysicalImpairment  hearingImpairment  breathingIssues  dyslexia given the following text: {text}",
    with open("llm/grammar.gbnf") as f:
        grammar = f.read()

    res = requests.post(
        url=os.getenv("LLMAPI_BASEURL")+"/completions",
        json={
        "prompt" : prompt,
        "grammar" : grammar,
        "max_tokens":0 # 0 is infinity
        }
    )
    outjson = json.loads(res.json()["choices"][0]["text"])
    return outjson