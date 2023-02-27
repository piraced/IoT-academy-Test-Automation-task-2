import json



def ReadConfigFile(filename):
    f = open(filename, "r")
    txtConfig = f.read()
    config = json.loads(txtConfig)
    return config

def FilterConfig(config, args):
    if args.EventTypes != None and len(args.EventTypes) > 0:
        newConfig = dict( tests=[])
        for test in config["tests"]:
            if test["eventType"] in args.EventTypes:
                newConfig["tests"].append(test)
    else:
        newConfig = config
    return newConfig


#no longer used
def SplitConfig(config):
    ruleConfig = []
    triggerConfig = []
    resultConfig = []
    for test in config["tests"]:
        ruleConfig.append(dict(
            eventType=test["eventType"],
            eventSubtype=test["eventSubtype"],
            endpoint=test["configuration"]["endpoint"],
            requestType=test["configuration"]["requestType"],
            parameters=test["configuration"]["parameters"]
        ))
        for index, config in enumerate(test["trigger"]):
            triggerConfig.append(dict(
                eventType=test["eventType"],
                eventSubtype=test["eventSubtype"],
                endpoint=test["trigger"][index]["endpoint"],
                requestType=test["trigger"][index]["requestType"],
                parameters=test["trigger"][index]["parameters"]
            ))
        resultConfig.append(dict(
            eventType=test["eventType"],
            eventSubtype=test["eventSubtype"],
            number=test["response"]["telephoneNumber"],
            text=test["response"]["text"]
        ))
    return [ruleConfig, triggerConfig, resultConfig]