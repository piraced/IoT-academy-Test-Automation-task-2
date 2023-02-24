import requests





def Login(ipAddress, username, password):
    login = {"username":username,"password":password}
    return requests.post("http://" + ipAddress + "/api/login", json=login).json()["ubus_rpc_session"]


def GetDeviceName(token, ip):
    request = {
        "endpoint": "/api/system/device/info",
        "requestType": "get",
        "parameters": {}
    }
    json = SendRequest(token, request, ip).json()
    return json["data"]["static"]["device_name"]

def CreateEventReport(token, config, ip):
    request = {
        "endpoint": "/api/services/events_reporting/config/",
        "requestType": "post",
        "parameters": {}
    }
    json = SendRequest(token, request, ip).json()
    id = json["data"]["id"]
    config["endpoint"] = config["endpoint"] + id
    config["parameters"]["data"]["id"] = id
    return SendRequest(token, config, ip).json()

def DeleteEventReport(token, id, ip):
    request = {
        "endpoint": "/api/services/events_reporting/config/",
        "requestType": "delete",
        "parameters": {
            "data":[id]
        }
    }
    return SendRequest(token, request, ip).json()
    

def SendRequest(token, requestInfo, ip):
    header = { "Authorization": "Bearer " + token}
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
            gdgagasg
    return response