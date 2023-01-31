import requests
import hashes as rh
import math
from datetime import datetime as DT
import time
import json
import asyncio
import discord
import aioschedule as s
import concurrent.futures


basicUrl = "https://api.raidreport.dev/raid/player/"
dungeonUrl= "https://api.raidreport.dev/dungeon/player/"
searchUrl = "https://api.raidreport.dev/search?q="
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.106'}
path = "C:/Users/mikop/Desktop/unstable/Elitist/db"
RRData={}
DRData={}
globalTimes = []
zarejestrowaneKonta = []
activeGuilds = []
raidClears=[]
speedrunRoles = []
clearLeaderboardChannels=[]

intents = discord.Intents.all()
client = discord.Client(intents=intents)

def fetch_RR_data(user_id):
    return requests.get(basicUrl+user_id, headers=headers).json()["response"]


def fetch_DR_data(user_id):
    return requests.get(basicUrl+user_id, headers=headers).json()["response"]


def requestData(): 
    global RRData
    global DRData
    start = DT.now()
    user_ids = [x[1] for x in zarejestrowaneKonta]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_data = {executor.submit(fetch_RR_data, user_id): user_id for user_id in user_ids}
        for future in concurrent.futures.as_completed(future_to_data):
            user_id = future_to_data[future]
            try:
                data = future.result()
            except Exception as exc:
                print(f'{user_id} generated an exception while fetching data: {exc}')
            else:
                RRData[user_id] = data
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_data = {executor.submit(fetch_DR_data, user_id): user_id for user_id in user_ids}
        for future in concurrent.futures.as_completed(future_to_data):
            user_id = future_to_data[future]
            try:
                data = future.result()
            except Exception as exc:
                print(f'{user_id} generated an exception while fetching data: {exc}')
            else:
                DRData[user_id] = data
    zapiszRRData()
    print(f"fetched data in {(DT.now()-start).total_seconds()}s")


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


def IDzaID(ID):
    if isinstance(ID, int):
        for x in zarejestrowaneKonta:
            if x[0] == ID:
                return x[1]
    if isinstance(ID, str):
        for x in zarejestrowaneKonta:
            if x[1] == ID:
                return x[0]
    return None


def updateStats(user):
    userInfo = RRData[user]
    userActivities = userInfo["activities"]
    czasyTablica = []
    for x in userActivities:
        y = x["activityHash"]
        if y in rh.raidHashes:
            raidDict = {
                "time": "5000",
                "raidName": "",
                "activityId": "",
                "userId": ""
            }
            if "fastestFullClear" in userActivities[userActivities.index(x)]["values"]:
                raidDict["time"] = userActivities[userActivities.index(x)]["values"]["fastestFullClear"]["value"]
                raidDict["raidName"] = rh.raidHashes[y]
                raidDict["activityId"] = userActivities[userActivities.index(x)]["values"]["fastestFullClear"]["instanceId"]
                raidDict["userId"] = userInfo["membershipId"]
            czasyTablica.append(raidDict)
    return (czasyTablica, userInfo['clearsRank']["value"])


def getCzasy(userList):
    returnList = []
    for x in userList: 
        #returnList.append(czasy(requests.get(basicUrl+x[1], headers=headers).json()["response"]["activities"]), x))
        stats=updateStats(x[1])
        returnList.append(stats[0])
    return returnList


async def updateCzasy(guild=None):
    global globalTimes
    czasy = getCzasy(zarejestrowaneKonta)
    if guild is None:
        for user in czasy:
            for raid in user:
                for fastest in globalTimes:
                    if raid["raidName"] == fastest["raidName"]:
                        if int(raid["time"]) < int(fastest["time"]):
                            fastest["time"] = raid["time"]
                            fastest["activityId"] = raid["activityId"]
                            times = fastest
                            zapisz()
                        break
    else:
        members = guild.members
        times = [{"time": 94001, "raidName": "DSC", "activityId": "11820595718", "userId": ""}, {"time": 12007, "raidName": "VOG", "activityId": "11924379516", "userId": ""}, {"time": 18807, "raidName": "KF", "activityId": "11789486698", "userId": ""}, {"time": 22007, "raidName": "VOD", "activityId": "11793229784", "userId": ""}, {"time": 7074, "raidName": "GOS", "activityId": "11849375285", "userId": ""}, {"time": 10833, "raidName": "MVOG", "activityId": "11306517279", "userId": ""}, {"time": 37035, "raidName": "MVOD", "activityId": "10726946750", "userId": ""}, {"time": 5009, "raidName": "LW", "activityId": "11798574719", "userId": ""}, {"time": 46205, "raidName": "MKF", "activityId": "11777367776", "userId": ""}]
        for p in czasy:
            for x in p:
                for y in times:
                    if x["raidName"] == y["raidName"]:
                        member = guild.get_member(IDzaID(x["userId"]))
                        if member is None or member not in members:
                            break
                        if int(x["time"]) < int(y["time"]):
                            y["time"] = x["time"]
                            y["activityId"] = x["activityId"]
                            zapisz()
                        break
        return times


async def rozdajRangi():
    for g in activeGuilds:
        roles = [x.name for x in await g.fetch_roles()]
        if "Speedrank: Challenger" not in roles:
            await g.create_role(name="Speedrank: Challenger", color=0xc74555)
        if "Speedrank: Master" not in roles:
            await g.create_role(name="Speedrank: Master", color=0xfa576f)
        if "Speedrank: Diamond" not in roles:
            await g.create_role(name="Speedrank: Diamond", color=0x048ab4)
        if "Speedrank: Gold" not in roles:
            await g.create_role(name="Speedrank: Gold", color=0xc99e03)

        for x in zarejestrowaneKonta:
            userInfo = RRData[x[1]]["speedRank"]
            member=await g.fetch_member(x[0])
            if userInfo['tier'] == "Gold":
                await member.add_roles(discord.utils.get(await g.fetch_roles(), name="Speedrank: Gold"))
            if userInfo['tier'] == "Diamond":
                await member.add_roles(discord.utils.get(await g.fetch_roles(), name="Speedrank: Diamond"))
            if userInfo['tier'] == "Master":
                await member.add_roles(discord.utils.get(await g.fetch_roles(), name="Speedrank: Master"))
            if userInfo['tier'] == "Challenger":
                await member.add_roles(discord.utils.get(await g.fetch_roles(), name="Speedrank: Challenger"))
        

async def ticker():
    while True:
        await rozdajRangi()
        requestData()
        await s.run_pending()
        await asyncio.sleep(300)


async def dodajKonto(bungieTag, userDiscordID):
    global zarejestrowaneKonta
    for x in zarejestrowaneKonta:
        if x[0] == userDiscordID:
            return "Jesteś już zarejestrowany"
    if "#" not in bungieTag:
        return "Nie znaleziono uzytkownika o podanej nazwie"
    nick = bungieTag[0:bungieTag.index("#")]
    tag = bungieTag[bungieTag.index("#")+1:]
    for x in requests.get(searchUrl+bungieTag, headers=headers).json()["response"]:
        if "bungieGlobalDisplayName" in x and x["bungieGlobalDisplayName"].upper() == nick.upper() and str(x["bungieGlobalDisplayNameCode"]) == tag:
            zarejestrowaneKonta.append((userDiscordID, x.get("membershipId")))
            zapisz()
            return f"Ustawiono Twoje konto na {bungieTag}"
    return "Nie znaleziono uzytkownika o podanej nazwie"


async def pokazTopCzasy(guild=None):
    returnString = ""
    if guild is not None:
        times = await updateCzasy(guild)
    else:
        await updateCzasy()
        times = globalTimes
    for x in times:
        name = x["raidName"]
        id = x["time"]
        activityId = x["activityId"]
        returnString = returnString + (f"{name:5} - [{timeFormat(id)}](https://raid.report/pgcr/{activityId})\n")
    return returnString


def fill_raid_clears():
    global raidClears
    raidClears = []
    for user in zarejestrowaneKonta:
        raidClears.append(updateStats(user[1])[1])
    zapiszRRData()


async def remove_all_roles(server, role_id):
    for member in server.members:
        try:
            await member.remove_role(role_id)
        except Exception as e:
            print(f"Failed to remove role from {member}: {e}")


async def ranksReset(server=None, checkOnly=False):
    global raidClears
    embed = discord.Embed(title = "Clear leaderboard", color = 0x000000)
    if len(raidClears) == 0:
        wczytajRRData()
        print(raidClears)
        embed.add_field(name="Empty", value="Probably an error occured or the bot has just reset")
        return embed
    deltaList=[]
    for user in zarejestrowaneKonta:
        deltaList.append([user[0], updateStats(user[1])[1]])
    for i in range(len(deltaList)):
        deltaList[i][1]=deltaList[i][1]-raidClears[i]
    deltaList = sorted(deltaList, key=lambda x: x[1])
    users = [f"<@{x[0]}>" for x in deltaList[:10]]
    clears = [str(x[1]) for x in deltaList[:10]]
    embed.add_field(name="Username", value="\n".join(users), inline=True)
    embed.add_field(name="Clears", value="\n".join(clears), inline=True)
    if not checkOnly:
        server=activeGuilds[0]
        members = server.members
        role = discord.utils.get(server.roles, id=1069412927695761458)
        members_to_remove_role = [m for m in members if 1069412927695761458 in [r.id for r in m.roles]]
        member_to_add_role = discord.utils.get(members, id=deltaList[0][0])
        for x in members_to_remove_role:
            await x.remove_roles(role)
        await member_to_add_role.add_roles(role)
        await server.get_channel(970493481598484540).send(content=f"<@{deltaList[0][0]}> had the most weekly clears: {deltaList[0][1]}!", embed=embed)
        fill_raid_clears()
    return embed


def wczytajGildie(list):
    global activeGuilds
    activeGuilds = list


def add(type, channel):
    if type == 0:
        speedrunRoles.append(channel)
    elif type == 1:
        clearLeaderboardChannels.append(channel)


def zapisz():
    with open(f"{path}/times.json", "w") as outfile:
        outfile.write(json.dumps(globalTimes))
    with open(f"{path}/accounts.json", "w") as outfile:
        outfile.write(json.dumps(zarejestrowaneKonta))


def wczytaj():
    with open(f"db/times.json", "r") as outfile:
        global globalTimes
        globalTimes = json.loads(outfile.read())
    with open(f"db/accounts.json", "r") as outfile:
        global zarejestrowaneKonta
        zarejestrowaneKonta = json.loads(outfile.read())


def zapiszRRData():
    with open(f"db/WeeklyRRData.json", "w") as outfile:
        outfile.write(json.dumps(raidClears))


def wczytajRRData():
    with open(f"db/WeeklyRRData.json", "r") as outfile:
        global raidClears
        l=json.loads(outfile.read())
        raidClears = l
    return l


def initialize(servers):
    wczytajGildie(servers)
    print("Gildie wczytane")
    wczytaj()
    print("Json wczytane")
    requestData()
    getCzasy(zarejestrowaneKonta)
    print("Data updated")
    print(servers)
    fill_raid_clears()
    print("Fully initialized")


s.every().tuesday.at("17:59").do(ranksReset)