#!/bin/python
import ConfigParser
import requests
import json
import urllib3
import time
import urllib2
import StringIO
from Pod.Pod import Pod

# initialize instance
config = ConfigParser.ConfigParser()

# read INI file
#config.readfp(open('config.ini'))
# getting ini file from git
req = urllib2.Request("https://raw.githubusercontent.com/nicholasttx/CronMon/dev/config.ini")
response = urllib2.urlopen(req)
iniContent = response.read()
strbuf = StringIO.StringIO(iniContent)
config.readfp(strbuf)


# get data
myToken = config.get("base_info", "token")

myUrl = config.get("base_info", "apiUrl")

# get namespace list
namespaces = config.get("namespaces", "namespaces").split(',')

# disable https certificate verify
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# get API call response
headers = {"Authorization": "Bearer {0}".format(myToken)}

# list for storing podsData
podsDataList = []


#####################################################################################
# loop the list to get pods in each namespace
for ns in namespaces:
    apiUrl = myUrl + "/api/v1/namespaces/{0}/pods".format(ns)
    podsData = requests.get(apiUrl, headers=headers,verify=False).json()
    podsDataList.append(podsData)

# Pod List which stores pods info
podsList = []

# looping podsDataList to get all pods states
for podData in podsDataList:
    for item in podData["items"]:
        # check if pod is at 'Running' state
        # if not, the report problems:
        if item["status"]["phase"].lower() != "running":
            # setting pod info
            myPod = Pod()
            myPod.name = item["metadata"]["name"]
            myPod.namespaces = item["metadata"]["namespace"]
            myPod.status = item["status"]["phase"]

            # adding pod info to the pod list
            podsList.append(myPod)

# let's do a print test
for pod in podsList:
    print "Pod name: {0}/{1}, Pod state: {2}".format(pod.namespace,pod.name,pod.state)

####################################################################################

# sleep the program
#time.sleep(20)
