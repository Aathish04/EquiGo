import requests
import urllib.parse
import os
from dotenv import load_dotenv
load_dotenv()

def queryWolfram(question):
    query = urllib.parse.quote_plus(question)
    print(query)
    ENDPOINT = f"https://api.wolframalpha.com/v1/result?i={query}&appid={os.getenv('WOLFRAM_APPID')}"
    a = requests.get(ENDPOINT)
    return a.text

def queries(PLACE="Chennai",DATE="today"):
    return  [
        f"Will it rain in {PLACE} on {DATE}?",
        f"Maximum temperature in {PLACE} on {DATE}?",
        f"Minimum temperature in {PLACE} on {DATE}?",
        f"UV index in {PLACE} on {DATE}?",
    ]
print(queryWolfram(queries()[3]))