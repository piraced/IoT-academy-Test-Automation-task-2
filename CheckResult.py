import datetime
import time

import SendHTTP


def GetAllSMS(token, ip, args):
    request = {
        "endpoint":"/api/services/mobile_utilities/sms_messages/read/config",
        "requestType":"get",
        "parameters": {}
        }
    return SendHTTP.SendRequest(token, request, ip, args).json()


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


def GetResponseSMS(token, ip2, number, text, date, args):
    for i in range(1, 11):
        response = GetAllSMS(token, ip2, args)
        sms = FindSMS(response, text)
        if sms == None:
            sms = NewerThanTimestampSMS(response, date)
        elif CheckSender(sms, number):
            return sms
        if sms != None and args.CorrectMessageWait == False:
            return sms
        time.sleep(args.MessageWait / 10)
    return sms
        


def CheckSender(sms, number):
    if sms["sender"] == number:
        return True
    else: 
        return False


def DeleteSMS(sms, token, ip, args):
    request = {
        "endpoint":"/api/services/mobile_utilities/sms_messages/read/config/" + sms["modem_id"] + "/" + sms["id"],
        "requestType":"delete",
        "parameters": {}
        }
    return SendHTTP.SendRequest(token, request, ip, args).json()

def CheckResult(test, sms):
    if sms == None:
        return False
    elif test["response"]["text"] == sms["message"] and test["response"]["telephoneNumber"] == sms["sender"]:
        return True
    else:
        return False