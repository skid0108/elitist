import requests
import hashes as rh
import math
import time
import json
import asyncio
import discord


basicUrl = "https://api.raidreport.dev/raid/player/4611686018489015592"
searchUrl = "https://api.raidreport.dev/search?q="
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.106'}

userInfo = requests.get(basicUrl, headers=headers).json()["response"]["activities"]


flawlessdict=rh.raidHashes.copy()
dict=rh.raidHashes.copy()
for x in userInfo:
    activityHash=x["activityHash"]
    if activityHash in rh.raidHashes:
        if "flawlessDetails" in x["values"]:
            min = 6
            for y in x["values"]["flawlessActivities"]:
                if (y["fresh"] == None or y["fresh"] == True):
                    if y["accountCount"] < min:
                        min = y["accountCount"]
            print(f'{rh.raidHashes[activityHash]} {min}')
            flawlessdict[activityHash] = min
        if "lowAccountCountActivities" in x["values"]:
            min = 6
            for y in x["values"]["lowAccountCountActivities"]:
                if y["accountCount"] < min:
                    min = y["accountCount"]
            print(f'{rh.raidHashes[activityHash]} {min}')
            dict[activityHash] = min

print(flawlessdict)
print(dict)