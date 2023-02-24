import argparse
import datetime
import os

import LoadConfig
import SendHTTP
import CheckResult
import WriteResult
import TerminalControl


def Main():
    args = argParser()
    #catch if cant connect
    bearerToken1 = SendHTTP.Login(args.ip1,args.Username1,args.Password1)
    bearerToken2 = SendHTTP.Login(args.ip2,args.Username2,args.Password2)

    if args.Router != SendHTTP.GetDeviceName(bearerToken1, args.ip1):
        raise Exception("Connected product (-ip1) is not the same as the product indicated as being tested (-r)")

    config = LoadConfig.SplitConfig(LoadConfig.FilterConfig(LoadConfig.ReadConfigFile("config.json"), args))
    writer = WriteResult.CreateResultFile()

    success = 0
    fail = 0

    for test in config:

        os.system('cls||clear')
        TerminalControl.PopulateTerminal(args.Router, test, success, fail, len(config))

        SendHTTP.SendRequest(bearerToken1, test[0], args.ip1)
        SendHTTP.SendRequest(bearerToken1, test[1], args.ip1)

        sms = CheckResult.GetResponseSMS(CheckResult.GetAllSMS(bearerToken2, test[2], args.ip2), test[2]["text"], datetime.datetime.now())
        
        WriteResult.WriteResult(test, sms, writer, CheckResult.CheckResult(test, sms))
        if CheckResult.CheckResult(test, sms):
            success+1
        else:
            fail+1

        #clean up (delete sms and event logging configuration)
        if sms != None:
            CheckResult.DeleteSMS(sms, bearerToken2, args.ip2)
        
    return 0



def argParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip1", required=True, help="IP address or url of the device being tested")
    parser.add_argument("-ip2", required=True, help="IP address or url of the device receiving event reports")
    parser.add_argument("-u1", "--Username1", required=True, help="Username to login to the router being tested")
    parser.add_argument("-u2", "--Username2", required=True, help="Username to login to the router recieving the event reports")
    parser.add_argument("-p1", "--Password1", required=True, help="Password to login to the router being tested")
    parser.add_argument("-p2", "--Password2", required=True, help="Password to login to the router recieving the event reports")
    parser.add_argument("-r", "--Router", required=True, help="The model of the router being tested")
    parser.add_argument("-t", "--Timeout", default=300, type=int, choices=range(10, 3601) ,help="The amount of time in seconds the test will wait to reestablish connection with the device being tested if it is disconnected during the test (for example: testing the reboot event reporting)")
    parser.add_argument("-mv", "--MessageWait", default=30, choices=range(3, 301), type=int, help="The amount of time in seconds the test will wait to recieve the SMS report")
    parser.add_argument("-cmv", "--CorrectMessageWait", action="store_true",help="Select if the test should keep waitng for the correct SMS for the rest of MessageWait duration after recieving a message with inccorect text or number (default:False)")
    parser.add_argument("-et", "--EventTypes", nargs='*', help="Event types to be tested")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    Main()