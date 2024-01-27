import requests
import urllib.parse as urlparse
from fastapi import FastAPI
from datetime import datetime
key = "qN86js1EGFaSWvQ28TASgkUuphaxAnbF"         # API Key

vehicletypes = {0:"car",1:"bus",2:"motorcycle",3:"bicycle",4:"pedestrian",5:"truck",6:"EV"}
def convertdatetime(dt=0):
    if dt == 0:
        #no parameter - current datetime
        dt = datetime.now()
    output_date = dt.strftime("%Y-%m-%dT%H:%M:%S")
    return output_date
       
       
app = FastAPI()

# Route parameters
                

async def getdata(jsonip):
    jsonip["start"] = await encode(jsonip["start"])
    jsonip["end"] = await encode(jsonip["end"])
    jsonip["routeType"] = "fastest"                        # Fastest route
    jsonip["traffic"] = "true"                             # To include Traffic information
    jsonip["travelMode"] = vehicletypes[jsonip["travelMode"]]                            # enum
    jsonip["avoid"] = "unpavedRoads"                       # Avoid unpaved roads
    # departAt = "2021-10-20T10:00:00"             # Departure date and time
    if jsonip["departAt"]== "null":
        #current time and date
        jsonip["departAt"] = convertdatetime()
    else:
        jsonip["departAt"] = convertdatetime(jsonip["departAt"])
    jsonip["vehicleCommercial"] = "true"                    # Commercial vehicle
    return jsonip

async def gettestdata():
    jsonip = {"start" : "Adyar, Chennai", 
          "end" : "Mylapore, Chennai" , 
          "routeType":"fastest",                      
          "traffic" : "true" ,
          "travelMode" :2 ,                   
          "avoid" : "unpavedRoads"  ,            
          "departAt" : "null",         
          "vehicleCommercial" : "true" } 
    return jsonip

@app.get("/")
async def root():
    
    return {"message": "hello world"}


@app.get("/routing")
async def travelroute():
    jsonip = await gettestdata()
    jsonip1 = await getdata(jsonip)
    baseUrl = "https://api.tomtom.com/routing/1/calculateRoute/"
    print(type(jsonip1["start"]))
    requestParams = (
    urlparse.quote(jsonip1["start"] ) + ":" + urlparse.quote(jsonip1["end"] ) 
    + "/json?routeType=" + jsonip1["routeType"]
    + "&traffic=" + jsonip1["traffic"]
    + "&travelMode=" + jsonip1["travelMode"]
    + "&avoid=" +  jsonip1["avoid"] 
    + "&vehicleCommercial=" + jsonip1["vehicleCommercial"]
    + "&departAt=" + urlparse.quote(jsonip1["departAt"]))
 
    requestUrl = baseUrl + requestParams + "&key=" + key
    print(requestUrl)
    response = requests.get(requestUrl)
    return {"message": response.json()}

@app.get("/encoding")
async def encode(location="Adyar, Chennai"):
    
    baseUrl = "https://api.tomtom.com/search/2/geocode"
    query= urlparse.quote(location)
 
    requestUrl = baseUrl + "/" + query+".json" + "?limit=1&key=" + key
    response = requests.get(requestUrl)
    r = response.json()
    r1=r["results"]
    latitude = r1[0]["position"]["lat"]
    longitude = r1[0]["position"]["lon"]
    st = str(latitude) + ","+ str(longitude)
    return st

@app.get("/EVrouting")
async def EVroute():
    jsonip = await gettestdata()
    jsonip1 = await getdata(jsonip)
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