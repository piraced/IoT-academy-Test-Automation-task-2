 # IoT-academy-Test-Automation-task-2
A Python 3.10 script to automate testing of the event reporting function on RUTos devices.

## Libraries
there is only one library being used:
* **requests 2.25.1**

## hardware requirements

* RUTos device being tested must be able to send SMS messages
* A 2nd RUTos device able to recieve SMS messages

## Launch arguments
All arguments for the program are flags, though some of them are mandatory and some are not

Mandatory arguments:
* **-ip1** - specifies the IP address or URL of the device being tested
* **-ip2** - specifies the IP address or URL of the device recieving the event report SMS messages
* **-u1 / --Username1** - username to login to the device being tested
* **-u2 / --Username2** - username to login to the device receiving SMS
* **-p1 / --Password1** - password to login to the device being tested
* **-p2 / --Password2** - password to login to the device receiving SMS
* **-r / --Router** - device name of the device being tested

Optional arguments:
* **-t / --Timeout** - time in seconds (between 10 and 3600, default - 300) the program will attempt to reestablish connection for
* **-mv / --MessageWait** - time in seconds (between 3 and 300, default - 30) the program will wait for the response SMS to arrive
* **-cmv / --CorrectMessageWait** - if this flag is used, the program will wait for the MessageWait period to recieve the expected SMS, otherwise - first SMS recieved after sending the requests to trigger the event report is assumed to be the response SMS
* **-et / --EventTypes** - A list of event types (sperated by spaces) that will be tested. If this flag is not used, then all the tests in the configuration file will be run.
* **-c / --Configuration** - The file name of the configuration file. Default: "config.json"

## Configuration file

example of a configuration file:

```
{
  "tests": [
    {
      "configuration": {
        "parameters": {
          "data": {
            "id": "",
            ".type": "rule",
            "event": "Config",
            "eventMark": "all",
            "action": "sendSMS",
            "enable": "1",
            "message": "test text",
            "recipient_format":"single",
            "telnum": "+37063674686"
          }
        }
      },
      "trigger": [
        {
          "endpoint": "/api/services/modbus/tcp_slave/config/general",
          "requestType": "put",
          "parameters": {
            "data": {
              ".type": "modbus",
              "id": "general",
              "keepconn": "1",
              "allow_ra": "0",
              "enabled": "1",
              "port": "502",
              "device_id": "1",
              "md_data_type": "0",
              "timeout": "0",
              "clientregs": "0"
            }
          }
        },
        {
          "endpoint": "/api/services/modbus/tcp_slave/config/general",
          "requestType": "put",
          "parameters": {
            "data": {
              ".type": "modbus",
              "id": "general",
              "keepconn": "1",
              "allow_ra": "0",
              "enabled": "0",
              "port": "502",
              "device_id": "1",
              "md_data_type": "0",
              "timeout": "0",
              "clientregs": "0"
            }
          }
        }
      ],
      "response": {
        "eventType": "Config Change",
        "eventSubtype": "all",
        "telephoneNumber": "+37066040956",
        "text": "test text"
      }
    }
  ]
}
```

The configuration file as an array of "tests". Each member of the "tests" array represents an Events Reporting to be tested. Each member of "tests" is then split into 3 parts: "configuration", "trigger" and "response"

#### "configuration"

This part of the config file simply holds the request payload to configure an instance of Events Reporting. 
Note that the id is not set as it is assigned randomly by the device and all of the fields in the example configuration are necessary

#### "trigger"

This part of the config file holds an array, of which each member contains the basic information to send a HTTP request: endpoint, request type and payload. Supported request types are: post, get, delete, put
The requests placed in this part are meant to trigger the Event Reporting rules and thus cause the response SMS to be sent.

#### "response"

This part of the config file holds the event type and subtype names which will be used in the output file as well as the expected SMS from the router being texted and from which number it is expected. Note that the number must be in full format icluding country coude and plus (for example: +370XXXXXXXX).

## Running the script

The script is launched by running the __Main.py__ file using Python. Other module files and the configuration file must be in the same folder.

After launching the script will run with no user input and generate a .csv file as output. The file will be automatically named following this convention: **deviceName_YYYY-MM-DD_HH:mm:ss.csv**

During runtime the console window will display some information about the ongoing testing
![image](https://user-images.githubusercontent.com/20305489/221588334-2c3b113b-0cab-487b-82f4-3812b1b213b4.png)

Note that while the script deletes the Events Reporting configuration and the received SMS, the actions taken to trigger the event report
are not automatically undone and if needed should be undone by adding more requests to the "trigger" section.
 
