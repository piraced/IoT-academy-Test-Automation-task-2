import csv
import datetime


def CreateResultFile(routerName):
    filename = routerName + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    file = open(filename, "a")
    writer = csv.writer(file)
    writer.writerow({"EVENT TYPE", "EVENT SUBTYPE", "EXPECTED MESSAGE", "RECEIVED MESSAGE", "EXPECTED NUMBER", "RECEIVED NUMBER", "RESULT"})
    return writer


def WriteResult(test, sms, writer, boolResult):
    if boolResult == True:
        result = "PASS"
    else:
        result = "FAIL"
        sms = {"message": "",
               "sender": ""}
    writer.writerow({test["response"]["eventType"], test["response"]["eventSubtype"], test["response"]["text"], sms["message"], test["response"]["telephoneNumber"], sms["sender"], result})
    return writer