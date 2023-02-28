import argparse
import datetime
import os

import LoadConfig
import SendHTTP
import CheckResult
import WriteResult
import TerminalControl

global bearerToken1
global bearerToken2

def Main():
    args = argParser()

    bearerToken1 = SendHTTP.Login(args.ip1,args.Username1,args.Password1)
    bearerToken2 = SendHTTP.Login(args.ip2,args.Username2,args.Password2)

    if args.Router != SendHTTP.GetDeviceName(bearerToken1, args):
        raise Exception("Device name given in the arguments does not match the device name of device at ip1")

    
    try:
        config = LoadConfig.FilterConfig(LoadConfig.ReadConfigFile(args.Config), args)
    except:
        os.system('cls||clear')
        print("The configuration file is missing or malformed")
        return 0
    
    writer = WriteResult.CreateResultFile(args.Router)

    success = 0
    fail = 0

    for test in config["tests"]:
        os.system('cls||clear')
        TerminalControl.PopulateTerminal(args.Router, test, success, fail, len(config["tests"]))

        ruleID = SendHTTP.CreateEventReport(bearerToken1, test["configuration"], args.ip1, args)["data"]["id"]
 
        for request in test["trigger"]:
            SendHTTP.SendRequest(bearerToken1, request, args.ip1, args)

        sms = CheckResult.GetResponseSMS(bearerToken2, args.ip2, test["response"]["telephoneNumber"], test["response"]["text"], datetime.datetime.now(), args)

        WriteResult.WriteResult(test, sms, writer, CheckResult.CheckResult(test, sms))
        if CheckResult.CheckResult(test, sms):
            success = success+1
        else:
            fail = fail+1

        print("a")
        input()

        if sms != None:
            CheckResult.DeleteSMS(sms, bearerToken2, args.ip2, args)
        SendHTTP.DeleteEventReport(bearerToken1, ruleID, args.ip1, args)
    os.system('cls||clear')
    TerminalControl.PopulateTerminal(args.Router, config["tests"][-1], success, fail, len(config["tests"]))
    return 0

#Rutx11 tel no - +37066040956
#Rut955 tel no - +37063674686
def argParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip1", required=True, help="IP address or url of the device being tested")
    parser.add_argument("-ip2", required=True, help="IP address or url of the device receiving event reports")
    parser.add_argument("-u1", "--Username1", required=True, help="Username to login to the router being tested")
    parser.add_argument("-u2", "--Username2", required=True, help="Username to login to the router recieving the event reports")
    parser.add_argument("-p1", "--Password1", required=True, help="Password to login to the router being tested")
    parser.add_argument("-p2", "--Password2", required=True, help="Password to login to the router recieving the event reports")
    parser.add_argument("-r", "--Router", required=True, help="The name of the device being tested")
    parser.add_argument("-t", "--Timeout", default=300, type=int, choices=range(10, 3601), metavar="10-3600" ,help="The amount of time in seconds the test will wait to reestablish connection with the device being tested if it is disconnected during the test (for example: testing the reboot event reporting)")
    parser.add_argument("-mv", "--MessageWait", default=30, choices=range(3, 301), type=int, metavar="3-300" ,help="The amount of time in seconds the test will wait to recieve the SMS report")
    parser.add_argument("-cmv", "--CorrectMessageWait", action="store_true",help="Select if the test should keep waitng for the correct SMS for the rest of MessageWait duration after recieving a message with inccorect text or number (default:False)")
    parser.add_argument("-et", "--EventTypes", nargs='*', help="Event types to be tested")
    parser.add_argument("-c", "--Config", default="config.json", help="File name of the configuration file. Default: config.json")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    Main()
