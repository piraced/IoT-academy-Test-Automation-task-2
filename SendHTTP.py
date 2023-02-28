import requests
import time
import os





def Login(ipAddress, username, password):
    login = {"username":username,"password":password}
    try:
        token = requests.post("http://" + ipAddress + "/api/login", json=login).json()["jwtToken"]
        token.raise_for_status()
    except requests.HTTPError as error:
        os.system('cls||clear')
        print("HTTP login request was unsuccessful with code: " + error.response.text)
        print("Please check the username and password and run the script again")
        quit()
    except requests.ConnectionError as error:
        os.system('cls||clear')
        print("There is a problem with the connection: " + error.response.text)
        quit()
    else:
        return token


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
    
#currently if the bearer token expires the program will start to re-login every request (and wait 1/10 of the timout)
#this would need a lot of refactoring to fix
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
            token = AttemptRelogin(ip, args)
        except requests.ConnectionError as error:
            os.system('cls||clear')
            print("There is a problem with the connection: " + error.response.text)
            print(f"Retrying...  ({i}/10)")
            token = AttemptRelogin(ip, args)
        else:
            return response
        time.sleep( args.Timeout / 10)
    return response


def AttemptRelogin(ip, args):
    if ip == args.ip1:
        return Login(ip, args.Username1, args.Password1)
    elif ip == args.ip2:
        return Login(ip, args.Username2, args.Password2)
    else: raise Exception