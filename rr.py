import requests
import hashes as rh
import math
import time
import json
import asyncio
import discord


basicUrl = "https://api.raidreport.dev/raid/player/"
searchUrl = "https://api.raidreport.dev/search?q="
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.106'}
globalTimes = []
zarejestrowaneKonta = []
intents = discord.Intents.all()
client = discord.Client(intents=intents)


def timeFormat(time):
    if time < 3600:
        return f'{math.floor(time/60)}m {time%60}s'
    else:
        return f'{math.floor(time/3600)}h {math.floor((time%3600)/60)}m {time%60}s'


def getKonto(membershipId):
    for x in zarejestrowaneKonta:
        if x[1] == membershipId:
            return x[0]
    return None


def czasy(user):
    userActivities = requests.get(basicUrl+user, headers=headers).json()["response"]["activities"]
    czasyTablica = []
    for x in userActivities:
        y = x["activityHash"]
        if y in rh.raidHashes:
            raidDict = {"time": "",
        "raidName": "",
        "activityId": ""}
            if "fastestFullClear" in userActivities[userActivities.index(x)]["values"]:
                raidDict["time"] = userActivities[userActivities.index(x)]["values"]["fastestFullClear"]["value"]
                raidDict["raidName"] = rh.raidHashes[y]
                raidDict["activityId"] = userActivities[userActivities.index(x)]["values"]["fastestFullClear"]["instanceId"]
            else:
                raidDict["time"] = "5000"
                raidDict["raidName"] = rh.raidHashes[y]
                raidDict["activityId"] = userActivities[userActivities.index(x)]["values"]["fastestFullClear"]["instanceId"]
            czasyTablica.append(raidDict)
    return czasyTablica


def getCzasy(userList):
    returnList = []
    for x in userList: 
        #returnList.append(czasy(requests.get(basicUrl+x[1], headers=headers).json()["response"]["activities"]), x))
        returnList.append(czasy(x[1]))
    return returnList


async def ticker():
    while True:
        print("ok")
        global globalTimes
        czasy = getCzasy(zarejestrowaneKonta)
        for p in czasy:
            for x in p:
                for y in globalTimes:
                    if x["raidName"] == y["raidName"]:
                        if int(x["time"]) < int(y["time"]):
                            y["time"] = x["time"]
                            y["activityId"] = x["activityId"]
                            zapisz()
                        break
        await asyncio.sleep(5)


def dodajKonto(url, userName):
    if "#" not in url:
        print("Nie znaleziono uzytkownika o podanej nazwie")
        return 0
    nick = url[0:url.index("#")]
    tag = url[url.index("#")+1:]
    for x in requests.get(searchUrl+url, headers=headers).json()["response"]:
        if "bungieGlobalDisplayName" in x and x["bungieGlobalDisplayName"].upper() == nick.upper() and str(x["bungieGlobalDisplayNameCode"]) == tag:
            global zarejestrowaneKonta
            zarejestrowaneKonta.append((userName, x.get("membershipId")))
            zapisz()
            return f"Ustawiono Twoje konto na {url}"
            #return requests.get(basicUrl+x['membershipId'], headers=headers).json()["response"]["activities"]
    return "Nie znaleziono uzytkownika o podanej nazwie"


def pokazTopCzasy():
    returnString = ""
    for x in globalTimes:
        name = x["raidName"]
        id = x["time"]
        activityId = x["activityId"]
        returnString = returnString + (f"{name} - [{timeFormat(id)}](https://raid.report/pgcr/{activityId})\n")
    return returnString



def zapisz():
    with open("C:/Users/mikop/Desktop/unstable/mechiza/db/times.json", "w") as outfile:
        outfile.write(json.dumps(globalTimes))
    with open("C:/Users/mikop/Desktop/unstable/mechiza/db/accounts.json", "w") as outfile:
        outfile.write(json.dumps(zarejestrowaneKonta))


def wczytaj():
    with open("C:/Users/mikop/Desktop/unstable/mechiza/db/times.json", "r") as outfile:
        global globalTimes
        globalTimes = json.loads(outfile.read())
    with open("C:/Users/mikop/Desktop/unstable/mechiza/db/accounts.json", "r") as outfile:
        global zarejestrowaneKonta
        zarejestrowaneKonta = json.loads(outfile.read())


wczytaj()
