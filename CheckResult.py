import datetime

import SendHTTP


def GetAllSMS(token, requestInfo, ip):
    request = {
        "endpoint":"/api/services/mobile_utilities/sms_messages/read/config",
        "requestType":"get",
        "parameters": {}
        }
    return SendHTTP.SendRequest(token, request, ip).json()


def FindSMS(response, text):
    for sms in response["data"]:
        if sms["message"] == text:
            return sms
    return None


def NewerThanTimestampSMS(response, date):
    if response["data"][0] and datetime.datetime.strptime(response["data"][0]["date"], "%c") >= date:
        return response["data"][0]
    else:
        return None


def GetResponseSMS(response, text, date, args):
    sms = FindSMS(response, text)
    if sms == None:
        sms = NewerThanTimestampSMS(response, date)


def CheckSender(sms, number):
    if sms["sender"] == number:
        return True
    else: 
        return False


def DeleteSMS(sms, token, ip):
    request = {
        "endpoint":"/api/services/mobile_utilities/sms_messages/read/config/" + sms["modem_id"] + "/" + sms["id"],
        "requestType":"delete",
        "parameters": {}
        }
    return SendHTTP.SendRequest(token, request, ip).json()

def CheckResult(test, sms):
    if sms == None:
        return False
    elif test[2]["text"] == sms["message"] and test[2]["number"] == sms["sender"]:
        return True
    else:
        return False