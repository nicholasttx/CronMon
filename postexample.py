#!/bin/python

import requests
import json
import urllib3


# disable https certificate verify
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# set token
myToken = "token"

apiUrl = "https://<nonitoring>/nrdp/"

baseData = {}

bodyList = []

jsonData = {"checkresult" : {"type" : "service", "checktype" : "1"},
            "hostname" : "<hostname>",
            "servicename" : "PODS_STATE",
            "state" : "1",
            "output" : "WARNING! THIS IS ANOTHER TEST o.O ~"
}

# adding data to list
bodyList.append(jsonData)

# adding data to dict
baseData["checkresults"] = bodyList

jsonData = json.dumps(baseData)

postData = {"cmd" : "submitcheck",
            "token" : myToken,
            "JSONDATA" : jsonData
}

# send POST
requests.post(apiUrl, data = postData, verify = False)

