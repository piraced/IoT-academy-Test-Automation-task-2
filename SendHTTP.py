import requests





def Login(ipAddress, username, password):
    login = {"username":username,"password":password}
    return requests.post("http://" + ipAddress + "/api/login", json=login).json()["ubus_rpc_session"]


def GetDeviceName(token, ip):
    request = {
        "endpoint": "",
        "requestType": "get",
        "parameters": {}
    }
    json = SendRequest(token, request, ip).json()
    return json["data"]["static"]["device_name"]


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