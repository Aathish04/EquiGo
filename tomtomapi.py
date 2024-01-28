import json
import requests
import urllib.parse as urlparse
from dotenv import load_dotenv
import os
load_dotenv()
from datetime import datetime
# from tomtomapi import get_data, get_test_data, encode
key = os.getenv("TOMTOMAPIKEY")

vehicletypes = {0:"car",1:"bus",2:"motorcycle",3:"bicycle",4:"pedestrian",5:"truck",6:"EV"}

from geopy.distance import geodesic
def filter_coordinates(coordinates, distance_threshold=500):
    filtered_coordinates = [coordinates[0]]

    for i in range(1, len(coordinates)):
        prev_coord = filtered_coordinates[-1]
        current_coord = coordinates[i]

        # Calculate distance between consecutive coordinates
        distance = geodesic(prev_coord, current_coord).meters

        if distance >= distance_threshold:
            filtered_coordinates.append(current_coord)

    return filtered_coordinates

def convertdatetime(dt=0):
    if dt ==0:
        #no parameter - current datetime
        dt = datetime.now()
    # if isinstance(dt,str):
    #     dt=datetime.strptime(dt)
    output_date = dt.strftime("%Y-%m-%dT%H:%M:%S")
    return output_date
       
# Route parameters
                
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
    
def coordinatesandinstr(t):
    
    print(t["message"])
    inst = []
    positions = []
    for i in t["message"]["routes"][0]["guidance"]["instructions"]:
        inst.append(i["message"])
        positions.append(i["point"])

    outputlist=[]
    # print(t["message"]["routes"][0]["legs"][0].keys())
    for i in t["message"]["routes"][0]["legs"][0]["points"]:
        outputlist.append((i["latitude"],i["longitude"]))
        
        # outputlist.append((temp[i]["points"]["latitude"],temp[i]["points"]["longitude"]))
        # outputlist[i].append(positions[i]["latitude"])
        # outputlist[i].append(positions[i]["longitude"])
    filter_coordinates(outputlist)

    return [inst,outputlist]

