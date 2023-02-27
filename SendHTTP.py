import requests
import time
import os





def Login(ipAddress, username, password):
    login = {"username":username,"password":password}
    return requests.post("http://" + ipAddress + "/api/login", json=login).json()["jwtToken"]


def GetDeviceName(token, args):
    request = {
        "endpoint": "/api/system/device/info",
        "requestType": "get",
        "parameters": {}
    }
    json = SendRequest(token, request, args.ip1, args).json()
    return json["data"]["static"]["device_name"]

def CreateEventReport(token, config, ip, args):
    request = {
        "endpoint": "/api/services/events_reporting/config/",
        "requestType": "post",
        "parameters": {}
    }
    json = SendRequest(token, request, ip, args).json()
    id = json["data"]["id"]
    request["endpoint"] = request["endpoint"] + id
    request["requestType"] = "put"
    request["parameters"] = config["parameters"]
    request["parameters"]["data"]["id"] = id
    return SendRequest(token, request, ip, args).json()

def DeleteEventReport(token, id, ip, args):
    request = {
        "endpoint": "/api/services/events_reporting/config/",
        "requestType": "delete",
        "parameters": {
            "data":[id]
        }
    }
    return SendRequest(token, request, ip, args).json()
    

def SendRequest(token, requestInfo, ip, args):
    header = { "Authorization": "Bearer " + token}
    for i in range (1, 11):
        try:
            match requestInfo["requestType"].lower():
                case "post":
                    response = requests.post("http://" + ip + requestInfo["endpoint"], headers=header, json=requestInfo["parameters"])
                case "get":
                    response = requests.get("http://" + ip + requestInfo["endpoint"], headers=header, json=requestInfo["parameters"])
                case "delete":
                    response =requests.delete("http://" + ip + requestInfo["endpoint"], headers=header, json=requestInfo["parameters"])
                case "put":
                    response = requests.put("http://" + ip + requestInfo["endpoint"], headers=header, json=requestInfo["parameters"])
                case other:
                    print("Incorrect/unsupported request type: " + requestInfo["requestType"])
            response.raise_for_status()
        except requests.HTTPError as error:
            os.system('cls||clear')
            print("HTTP request was unsuccessful with code: " + error.response.text)
            print(f"Retrying...  ({i}/10)")
        except requests.ConnectionError as error:
            os.system('cls||clear')
            print("There is a problem with the connection: " + error.response.text)
            print(f"Retrying...  ({i}/10)")
        else:
            return response
        time.sleep( args.Timeout / 10)
    return response