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

def queries():
    return  [
        "Will it rain in PLACE on DATE?",
        "Maximum temperature in PLACE on DATE?",
        "Minimum temperature in PLACE on DATE?",
        "UV index in PLACE on DATE?",
        
    ]
print(queryWolfram("Average Electric Vehicle Mileage?",))