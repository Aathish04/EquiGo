import json
import requests
import urllib.parse as urlparse
from fastapi import FastAPI
from dotenv import load_dotenv
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
    + "&departAt=" + urlparse.quote(departAt))
 
    requestUrl = baseUrl + requestParams + "&key=" + key
    print(requestUrl)
    response = requests.get(requestUrl)
    return {"message": response.json()}


@app.get("/EVrouting")
async def EVroute():
    # jsonip = await tomtomapi.gettestdata()
    # jsonip1 = await tomtomapi.getdata(jsonip)
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
    locations = jsonip1["start"] + ":" + jsonip1["end"]
    response = requests.post(
        f'https://api.tomtom.com/routing/1/calculateLongDistanceEVRoute/{locations}/json?key=qN86js1EGFaSWvQ28TASgkUuphaxAnbF&vehicleEngineType=electric&constantSpeedConsumptionInkWhPerHundredkm=32,10.87:77,18.01&currentChargeInkWh=20&maxChargeInkWh=40&minChargeAtDestinationInkWh=4&minChargeAtChargingStopsInkWh=4',
        headers=headers,
        json=json_data,
    )
    return {"message": response.json()}

# Translation 
