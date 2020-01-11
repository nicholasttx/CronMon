#!/bin/python
import ConfigParser
import requests
import json
import urllib3

# initialize instance
config = ConfigParser.ConfigParser()

# read INI file
config.readfp(open('config.ini'))


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

# loop the list to get pods in each namespace
for ns in namespaces:
   apiUrl = myUrl + "/api/v1/namespaces/{0}/pods".format(ns)
   podsData = requests.get(apiUrl, headers=headers).json()
   podsDataList.append(podsData)

#print podsData['items'][1]['status']['phase']
#print len(podsData["items"][0]["metadata"])

# looping podsDataList to get all pods states
for podData in podsDataList:
    for item in podData["items"]:
#        print "Pod Name: {0}/{1} -- Pod State: {2}".format(item["metadata"]["namespace"],item["metadata"]["name"], item["status"]["phase"])
        # writing data in to a file
        with open('resuilt.txt', 'a') as f:
            f.write("Pod Name: {0}/{1} -- Pod State: {2} \n".format(item["metadata"]["namespace"],item["metadata"]["name"], item["status"]["phase"]))

