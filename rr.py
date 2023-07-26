import hashes as rh
import logging_private
import enums as enums
import grading_system as GS

import os
import requests
import math
from datetime import datetime as DT
import json
import asyncio
import discord
import aioschedule as s
import concurrent.futures

log = logging_private.Logging(f"{os.getcwd()}/logs.txt")
log.log("Application started")

rr_url = "https://api.raidreport.dev/raid/player/"
dr_url= "https://api.raidreport.dev/dungeon/player/"
search_url = "https://api.raidreport.dev/search?q="
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.106'}
registered_accounts = []
active_guilds = []
weekly_raid_clears={}
rr_speedrank_roles = []
channels_clear_leaderboard=[]
intents = discord.Intents.all()
client = discord.Client(intents=intents)

ORACLE = None
RANKS = {}


class USER:
    discord_id = int
    rr_id = str
    rr_data = None
    raid_clears = int
    speed_rank = str
    weekly_data = None

    def __init__(self, rrid, data):
        self.rr_id = rrid
        #self.discord_id = data
        self.discord_id = data['discord_id']
        if data['weekly_raids'] is None:
            print("none found")
            self.update_rr_data()
            self.weekly_data = self.raid_clears
        else:
            self.weekly_data = data["weekly_raids"]
        
    def __del__(self):
        log.log(f"Deleted object USER with RRID {self.rr_id}")

    def __str__(self):
        return f"RRID: {self.rr_id}, DID: {self.discord_id}"
    
    def update_rr_data(self):
        self.rr_data = requests.get(rr_url+self.rr_id, headers=headers).json()["response"]
        self.raid_clears = self.rr_data['clearsRank']["value"]
        self.speed_rank = self.rr_data['speedRank']['tier']
        
    def set_weekly_raid(self, value):
        self.weekly_data = value
        
    def new_week(self):
        self.weekly_data = self.raid_clears


async def OBCZAJ_RANGI():
    global RANKS
    RANKS = {
    "Gold": discord.utils.get(await ORACLE.fetch_roles(), name="Speedrank: Gold"),
    "Diamond": discord.utils.get(await ORACLE.fetch_roles(), name="Speedrank: Diamond"),
    "Master": discord.utils.get(await ORACLE.fetch_roles(), name="Speedrank: Master"),
    "Challenger": discord.utils.get(await ORACLE.fetch_roles(), name="Speedrank: Challenger")
}


def fetch_RR_data(user_id):
    return requests.get(rr_url+user_id, headers=headers).json()["response"]


def request_data():
    log.logst("request_data")
    global registered_accounts
    start = DT.now()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_user = {executor.submit(user.update_rr_data): user for user in registered_accounts}
        for future in concurrent.futures.as_completed(future_to_user):
            user = future_to_user[future]
            try:
                future.result()
            except Exception as exc:
                log.logerr("fetch_data", f'{exc} ({user})')
    log.log(f"fetched data in {(DT.now()-start).total_seconds()}s")
    log.logend("request_data")



def timeFormat(time):
    if time < 3600:
        return f'{math.floor(time/60)}m {time%60}s'
    return f'{math.floor(time/3600)}h {math.floor((time%3600)/60)}m {time%60}s'


def convert_id(ID):
    if isinstance(ID, int):
        for x in registered_accounts:
            if x.discord_id == ID:
                return x.rr_id
    if isinstance(ID, str):
        for x in registered_accounts:
            if x.rr_id == ID:
                return x.discord_id
    return None


def user_best_times(user):
    log.logst("user_best_times")
    user_activities = user.rr_data["activities"]
    raid_times = {}
    for activity in user_activities:
        activity_hash = activity["activityHash"]
        if activity_hash in rh.raidHashes:
            best_raid_time = {"time": None, "raidName": rh.raidHashes[activity_hash]}
            if "fastestFullClear" in user_activities[user_activities.index(activity)]["values"]:
                best_raid_time["time"] = user_activities[user_activities.index(activity)]["values"]["fastestFullClear"]["value"]
                best_raid_time["activityId"] = user_activities[user_activities.index(activity)]["values"]["fastestFullClear"]["instanceId"]
                best_raid_time["userId"] = user.discord_id
            raid_times[activity_hash] = best_raid_time
    user_times = {
        "user_discord_id": user.discord_id,
        "user_raid_times": raid_times
    }
    log.logend("user_best_times")
    return (user_times)


def best_times(user_list):
    log.logst("best_times")
    #returnList = []
    #for x in userList: 
    #    stats=user_best_times(x)
    #    returnList.append(stats)
    log.logend("best_times")
    return [user_best_times(x) for x in user_list]



async def times_leaderboard(guild=None):
    log.logst("times_leaderboard")
    czasy = best_times(registered_accounts)

    fastest_raids={}

    if guild is not None:
        members = [x.id for x in guild.members]
    else:
        members = [x.discord_id for x in registered_accounts]
    
    for user_times in czasy:
        if user_times["user_discord_id"] not in members:
            continue

        for activity in user_times["user_raid_times"]:
            if user_times['user_raid_times'][activity]["time"] is None:
                continue

            if activity not in fastest_raids:
                fastest_raids[activity] =  user_times['user_raid_times'][activity]
                continue
            if int(user_times['user_raid_times'][activity]["time"]) < int(fastest_raids[activity]["time"]):
                fastest_raids[activity] = user_times['user_raid_times'][activity]
    log.logend("times_leaderboard")
    return fastest_raids


async def print_speedrun_leaderboard(guild=None):
    log.logst("print_speedrun_leaderboard")
    returnString = ""

    times = await times_leaderboard(guild)
        
    for raid in times:
        name = rh.raidHashes[raid]
        time = times[raid]["time"]
        activityId = times[raid]["activityId"]
        returnString = returnString + (f"{name:<5} - [{timeFormat(time)}](https://raid.report/pgcr/{activityId})\n")
    log.logend("print_speedrun_leaderboard")
    return returnString


async def update_ranks():
    log.logst("update_ranks")
    for g in active_guilds:
        roles = [x.name for x in await g.fetch_roles()]
        if "Speedrank: Challenger" not in roles:
            await g.create_role(name="Speedrank: Challenger", color=0xc74555)
        if "Speedrank: Master" not in roles:
            await g.create_role(name="Speedrank: Master", color=0xfa576f)
        if "Speedrank: Diamond" not in roles:
            await g.create_role(name="Speedrank: Diamond", color=0x048ab4)
        if "Speedrank: Gold" not in roles:
            await g.create_role(name="Speedrank: Gold", color=0xc99e03)

        for user in registered_accounts:
            try:
                member = await g.fetch_member(user.discord_id)
            except Exception as exc:
                log.logerr("update_ranks", exc)
                continue
            if RANKS[user.speed_rank] not in member.roles:
                try:
                    for x in RANKS:
                        await member.remove_roles(RANKS[x])
                    await member.add_roles(RANKS[user.speed_rank])
                except Exception as exc:
                    log.logerr("update_ranks", exc)
    log.logend("update_ranks")

async def ticker():
    while True:
        log.logst("ticker")
        wczytaj()
        await update_ranks()
        await s.run_pending()
        request_data()
        await asyncio.sleep(900)
        log.logend("ticker")


def dodajKonto(membershipID, userDiscordID):
    log.logst("dodaj_konto")
    global registered_accounts
    #for x in zarejestrowaneKonta:
    #    if x[0] == userDiscordID:
    #        return "Jesteś już zarejestrowany"
    #if "#" not in bungieTag:
    #    return "Nie znaleziono uzytkownika o podanej nazwie"
    #nick = bungieTag[0:bungieTag.index("#")]
    #tag = bungieTag[bungieTag.index("#")+1:]
    #for x in requests.get(searchUrl+bungieTag, headers=headers).json()["response"]:
    #    if "bungieGlobalDisplayName" in x and x["bungieGlobalDisplayName"].upper() == nick.upper() and str(x["bungieGlobalDisplayNameCode"]) == tag:
    #        zarejestrowaneKonta.append([userDiscordID, x.get("membershipId")])
    #        zapisz()
    #        print(zarejestrowaneKonta)
    #        return f"Ustawiono Twoje konto na {bungieTag}"
    #return "Nie znaleziono uzytkownika o podanej nazwie"
    wczytaj()
    if membershipID not in registered_accounts:
        registered_accounts[membershipID] = int(userDiscordID)
        zapisz()
    log.logend("dodaj_konto")


def reset_weekly_raid_clears():
    log.logst("reset_weekly_raid_clears")
    request_data()
    for user in registered_accounts:
        user.new_week()
    zapisz()
    log.logend("reset_weekly_raid_clears")


async def ranksReset(server=None, checkOnly=False):
    log.logst("ranks_reset")
    embed = discord.Embed(title = "Clear leaderboard", color = 0x000000)
    #if len(weekly_raid_clears) == 0:
    #    wczytajRRData()
    #    embed.add_field(name="Empty", value="Probably an error occured or the bot has just reset")
    #    log.logend("ranks_reset")
    #    return embed
        
    deltaList={}
    for x in registered_accounts:
        deltaList[x.discord_id] = x.raid_clears - x.weekly_data
        
    delta_list_sorted = sorted(deltaList.items(), key=lambda x: x[1], reverse=True)
    embedBody = ""
    
    for x in range(0, 10):
        embedBody=embedBody+(f"{delta_list_sorted[x][1]} - <@{delta_list_sorted[x][0]}>\n")
    embed.add_field(name="Stats", value=embedBody, inline=True)
    
    if not checkOnly:
        server=active_guilds[0]
        members = server.members
        role = discord.utils.get(server.roles, id=1069412927695761458)
        members_to_remove_role = [m for m in members if 1069412927695761458 in [r.id for r in m.roles]]
        member_to_add_role = discord.utils.get(members, id=delta_list_sorted[0][0])
        for x in members_to_remove_role:
            await x.remove_roles(role)
        await member_to_add_role.add_roles(role)
        await server.get_channel(970493481598484540).send(content=f"<@{delta_list_sorted[0][0]}> had the most weekly clears: {delta_list_sorted[0][1]}!", embed=embed)
        reset_weekly_raid_clears()
    log.logend("ranks_reset")
    return embed


def overall_grade(discord_id):
    for x in registered_accounts:
        if x.discord_id == discord_id:
            return GS.get_score(x.rr_data)


def wczytajGildie(list):
    log.logst("wczytajGildie")
    global active_guilds
    active_guilds = list
    log.logend("wczytajGildie")


def add(type, channel):
    if type == 0:
        rr_speedrank_roles.append(channel)
    elif type == 1:
        channels_clear_leaderboard.append(channel)


def zapisz():
    with open(f"db/accounts.json", "w") as outfile:
        save = {}
        for x in registered_accounts:
            save[x.rr_id] = {
                'discord_id': x.discord_id,
                'weekly_raids': x.weekly_data
            }
        outfile.write(json.dumps(save))


def wczytaj():
    with open(f"db/accounts.json", "r") as outfile:
        global registered_accounts
        users = json.loads(outfile.read())
        for new in users:
            for reg in registered_accounts:
                if new == reg.rr_id:
                    break
            else:
                registered_accounts.append(USER(new, users[new]))


# old databases, dont use unless a disaster strikes
#def zapiszRRData():
#    with open(f"db/WeeklyRRData.json", "w") as outfile:
#        ret = {}
#        for x in registered_accounts:
#            ret[x.rr_id] = x.weekly_data
#        outfile.write(json.dumps(ret))
#
#
#def wczytajRRData():
#    with open(f"db/WeeklyRRData.json", "r") as outfile:
#        data=json.loads(outfile.read())
#        for value in data:
#            for user in registered_accounts:
#                if user.rr_id == value:
#                    user.set_weekly_raid(data[value])
#                    break


async def initialize(servers):
    wczytajGildie(servers)
    print("Gildie wczytane")
    wczytaj()
    print("Json wczytane")
    request_data()
    print("Data downloaded")
    zapisz()
    best_times(registered_accounts)
    print("Data updated")
    global ORACLE
    ORACLE = servers[0]
    await OBCZAJ_RANGI()
    print("Discord ranks loaded")
    print("Fully initialized, ready to serve")


s.every().tuesday.at("18:59").do(ranksReset)
