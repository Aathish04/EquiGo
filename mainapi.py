import json
import requests
import urllib.parse as urlparse
from urllib.parse import unquote
from fastapi import FastAPI,Request
from dotenv import load_dotenv
from pprint import pprint
import os
load_dotenv()
# from tomtomapi import get_data, get_test_data, encode
import tomtomapi
app = FastAPI()
key = os.getenv("TOMTOMAPIKEY")

@app.get("/")
async def root(string):
    
    return {"message": json.loads(string)}


@app.get("/routing")
async def travelroute(start,end,departAt=None,travelMode="car",routeType="fastest",traffic="true",avoid="unpavedRoads",vehicleCommercial="true"):
    # jsonip = await tomtomapi.gettestdata()
    # jsonip1 = await tomtomapi.getdata(jsonip)
    start = str(await tomtomapi.encode(start))
    end = str(await tomtomapi.encode(end))
    if departAt== None:
        #current time and date
        departAt = tomtomapi.convertdatetime()
    else:
        departAt = tomtomapi.convertdatetime(departAt)

    baseUrl = "https://api.tomtom.com/routing/1/calculateRoute/"
    # print(type(jsonip1["start"]))
    requestParams = (
    urlparse.quote(start) + ":" + urlparse.quote(end) 
    + "/json?routeType=" + routeType
    + "&traffic=" + traffic
    + "&travelMode=" + travelMode
    + "&avoid=" +  avoid
    + "&vehicleCommercial=" + vehicleCommercial
    + "&instructionsType=" + "text"
    + "&departAt=" + urlparse.quote(departAt))
    
 
    requestUrl = baseUrl + requestParams + "&key=" + key
    print(requestUrl)
    response = requests.get(requestUrl)
    return {"message": response.json()}


@app.get("/EVrouting")
async def EVroute(start,end):
    # jsonip = await tomtomapi.gettestdata()
    # jsonip1 = await tomtomapi.getdata(jsonip)
    start = str(await tomtomapi.encode(start))
    end = str(await tomtomapi.encode(end))
    headers = {
    'Content-Type': 'application/json',
}

    json_data = {
        'chargingParameters': {
            'batteryCurve': [
                {
                    'stateOfChargeInkWh': 50.0,
                    'maxPowerInkW': 200,
                },
                {
                    'stateOfChargeInkWh': 70.0,
                    'maxPowerInkW': 100,
                },
                {
                    'stateOfChargeInkWh': 80.0,
                    'maxPowerInkW': 40,
                },
            ],
            'chargingConnectors': [
                {
                    'currentType': 'AC3',
                    'plugTypes': [
                        'IEC_62196_Type_2_Outlet',
                        'IEC_62196_Type_2_Connector_Cable_Attached',
                        'Combo_to_IEC_62196_Type_2_Base',
                    ],
                    'efficiency': 0.9,
                    'baseLoadInkW': 0.2,
                    'maxPowerInkW': 11,
                },
                {
                    'currentType': 'DC',
                    'plugTypes': [
                        'IEC_62196_Type_2_Outlet',
                        'IEC_62196_Type_2_Connector_Cable_Attached',
                        'Combo_to_IEC_62196_Type_2_Base',
                    ],
                    'voltageRange': {
                        'minVoltageInV': 0,
                        'maxVoltageInV': 500,
                    },
                    'efficiency': 0.9,
                    'baseLoadInkW': 0.2,
                    'maxPowerInkW': 150,
                },
                {
                    'currentType': 'DC',
                    'plugTypes': [
                        'IEC_62196_Type_2_Outlet',
                        'IEC_62196_Type_2_Connector_Cable_Attached',
                        'Combo_to_IEC_62196_Type_2_Base',
                    ],
                    'voltageRange': {
                        'minVoltageInV': 500,
                        'maxVoltageInV': 2000,
                    },
                    'efficiency': 0.9,
                    'baseLoadInkW': 0.2,
                },
            ],
            'chargingTimeOffsetInSec': 60,
        },
    }
    locations = "lat,long:lat,long"
    locations = start+ ":" + end
    response = requests.post(
        f'https://api.tomtom.com/routing/1/calculateLongDistanceEVRoute/{locations}/json?key=qN86js1EGFaSWvQ28TASgkUuphaxAnbF&vehicleEngineType=electric&constantSpeedConsumptionInkWhPerHundredkm=32,10.87:77,18.01&currentChargeInkWh=20&maxChargeInkWh=40&minChargeAtDestinationInkWh=4&minChargeAtChargingStopsInkWh=4',
        headers=headers,
        json=json_data,
    )
    return {"message": response.json()}

@app.get("/entopref")
async def entopref(jsonip):
    jsonip = json.loads(jsonip)
    lan = jsonip["pref_lan"]
    text = jsonip["text"]

    headers = {
        'authority': 'demo-api.models.ai4bharat.org',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://models.ai4bharat.org',
        'referer': 'https://models.ai4bharat.org/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    json_data = {
        'controlConfig': {
            'dataTracking': True,
        },
        'input': [
            {
                'source': text,
            },
        ],
        'config': {
            'serviceId': '',
            'language': {
                'sourceLanguage': 'en',
                'targetLanguage': lan,
                'targetScriptCode': None,
                'sourceScriptCode': None,
            },
        },
    }

    response = requests.post('https://demo-api.models.ai4bharat.org/inference/translation/v2', headers=headers, json=json_data)

    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    #data = '{"controlConfig":{"dataTracking":true},"input":[{"source":"Hello"}],"config":{"serviceId":"","language":{"sourceLanguage":"en","targetLanguage":"hi","targetScriptCode":null,"sourceScriptCode":null}}}'
    #response = requests.post('https://demo-api.models.ai4bharat.org/inference/translation/v2', headers=headers, data=data)
    # response = requests.post(
    # API_URL,
    # json={"text": text,"source_language": "en","target_language": lan},
    # )
    return json.loads(response.text)

@app.get("/preftoen")
async def preftoen(jsonip):
    jsonip = json.loads(jsonip)
    lan = jsonip["pref_lan"]
    text = jsonip["data"]

    headers = {
        'authority': 'demo-api.models.ai4bharat.org',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://models.ai4bharat.org',
        'referer': 'https://models.ai4bharat.org/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    json_data = {
        'controlConfig': {
            'dataTracking': True,
        },
        'input': [
            {
                'source': text,
            },
        ],
        'config': {
            'serviceId': '',
            'language': {
                'sourceLanguage': lan,
                'targetLanguage': "en",
                'targetScriptCode': None,
                'sourceScriptCode': None,
            },
        },
    }

    response = requests.post('https://demo-api.models.ai4bharat.org/inference/translation/v2', headers=headers, json=json_data)

    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    #data = '{"controlConfig":{"dataTracking":true},"input":[{"source":"Hello"}],"config":{"serviceId":"","language":{"sourceLanguage":"en","targetLanguage":"hi","targetScriptCode":null,"sourceScriptCode":null}}}'
    #response = requests.post('https://demo-api.models.ai4bharat.org/inference/translation/v2', headers=headers, data=data)
    # response = requests.post(
    # API_URL,
    # json={"text": text,"source_language": "en","target_language": lan},
    # )
    return json.loads(response.text)

@app.post("/stt")
async def stt(request: Request):
    body = await request.body()
    jsonip = json.loads(body)
    
    lan = jsonip["pref_lan"]
    audio = jsonip["data"]

    headers = {
        'authority': 'demo-api.models.ai4bharat.org',
        'accept': '*/*',
        'accept-language': 'en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://models.ai4bharat.org',
        'referer': 'https://models.ai4bharat.org/',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    json_data = {
        'config': {
            'language': {
                'sourceLanguage': lan,
            },
            'transcriptionFormat': {
                'value': 'transcript',
            },
            'audioFormat': 'wav',
            'samplingRate': '16000',
            'postProcessors': None,
        },
        'audio': [
            {
                'audioContent': audio 
                },
        ],
        'controlConfig': {
            'dataTracking': True,
        },
    }

    response = requests.post('https://demo-api.models.ai4bharat.org/inference/asr/conformer', headers=headers, json=json_data)
    return response.json()

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.


@app.post("/planroute")
async def planroute(request: Request):
    body = (await request.body()).decode("utf-8")
    jsonip = json.loads(body)
    print(jsonip)
    lan = jsonip["pref_lan"]
    isaudio = jsonip["isaudio"]
    data = jsonip["data"]
    response = jsonip["data"]
    # input()
    if isaudio== True :
        print("#################################")
        headers = {
        'authority': 'demo-api.models.ai4bharat.org',
        'accept': '*/*',
        'accept-language': 'en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://models.ai4bharat.org',
        'referer': 'https://models.ai4bharat.org/',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }

        json_data = {
            'config': {
                'language': {
                    'sourceLanguage': lan,
                },
                'transcriptionFormat': {
                    'value': 'transcript',
                },
                'audioFormat': 'wav',
                'samplingRate': '16000',
                'postProcessors': None,
            },
            'audio': [
                {
                    'audioContent': data 
                    },
            ],
            'controlConfig': {
                'dataTracking': True,
            },
        }

        response = requests.post('https://demo-api.models.ai4bharat.org/inference/asr/conformer', headers=headers, json=json_data)

    elif lan != "en":
        # jsonip["data"]= unquote(jsonip["data"]);
        
        # print(jsonip)
        response = await preftoen(json.dumps(jsonip))
        print(response)
        return response["output"][0]["target"]
    
    else:
        response = jsonip["data"]
    if (isinstance(response,str)):
        return response
    return response.json()

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
