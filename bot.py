import os
import discord
from discord import app_commands
import asyncio
from random import randint
import enums as p
import rr as rr

TOKEN = "NzkxMzE2MjAyOTc0MjE2MjQy.X-NYpA.hYCliU9r1uKyFI7jlYOEzHPyN-o"
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
activeEvents = []


class Event:
    message = None
    members = []
    raidName = ""
    raidType = 0
    wiad = None

    def __init__(self, eRaid):
        self.raidName = eRaid
        self.raidType = p.raidSwitch[eRaid]
        self.members = p.raidMembers[self.raidType]
        print(self.members)

    def __del__(self):
        activeEvents.remove((self, self.message))

    def update(self, mID, wiad):
        self.message = mID
        self.wiad = wiad
        activeEvents.append((self, self.message))

    def Embed(self):
        rtn = discord.Embed(title = self.raidName, color = 0xff0000)
        roleString = ""
        for x in self.members:
            roleString=roleString+f"{x[0]}:  {x[1]}\n"
        rtn.add_field(name = "Role:", value = roleString, inline = False)
        rtn.set_footer(text="Zbieramy się jak wszystkie miejsca będą pełne")
        #rtn.add_field(name = "Cut:", value = f"{self.cut}$", inline = True)
        #rtn.add_field(name = "Class:", value = f"{self.klasa}", inline = True)
        return rtn

    async def Dodaj(self, numer, kto):
        if self.members[numer][1] != "":
            for x in self.members:
                if x[1] == kto:
                    return
            self.members[numer] = (self.members[numer][0], kto)
            await self.wiad.edit(embed=self.Embed())
        
        

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(name="you fail", type=3))
    await tree.sync(guild=discord.Object(id=968943687272898612))
    await rr.ticker()


@client.event
async def on_message(message):
    if "RATIO" in message.content.upper():
        await message.channel.send(p.ratio[randint(1, len(p.ratio))])

    elif "WE LOSUJ RAIDA" in message.content.upper():
        await message.channel.send("pog, twój raid to...")
        await asyncio.sleep(1)
        await message.channel.send(p.raidyRandom[randint(1, len(p.raidyRandom))])


@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return
    for x in activeEvents:
        if payload.message_id == x[1]:
            print(payload.emoji.name)
            if payload.emoji.name in p.emojiList:
                print("ok")
                await x[0].Dodaj(p.emojiList.index(payload.emoji.name), payload.member.display_name)
            return
    

@tree.command(name = "event", description = "zrob event", guild=discord.Object(id=968943687272898612))
@app_commands.choices(raid=[
        app_commands.Choice(name="KF", value="KF"),
        app_commands.Choice(name="VoD", value="VoD"),
        app_commands.Choice(name="VoG", value="VoG"),
        app_commands.Choice(name="DSC", value="DSC"),
        app_commands.Choice(name="GoS", value="GoS"),
        app_commands.Choice(name="LW", value="LW"),])
async def first_command(interaction, raid: app_commands.Choice[str]):
    temp = Event(raid.value)
    await interaction.response.send_message(content = "<@&1021880510550659102>",embed=temp.Embed())
    mID = await interaction.original_response()
    #print(mID.id)
    temp.update(mID.id, mID)
    for x in p.emojiList:
        await mID.add_reaction(x)


@tree.command(name = "register", description = "link your Discord account with your bungie.net", guild=discord.Object(id=968943687272898612))
async def second_command(interaction, tag: str):
    await interaction.response.send_message(rr.dodajKonto(tag, interaction.user.id))


@tree.command(name = "times", description = "Show best times", guild=discord.Object(id=968943687272898612))
async def second_command(interaction):
    embed = discord.Embed(title = "Best raid times", color = 0x000000)
    embed.set_footer(text="Brought to you by Destinuś",icon_url="https://www.bungie.net/common/destiny2_content/icons/3c251b702026fee24488eac5cbd3a2e2.jpg")
    embed.add_field(name = "Click on the times for RR page",value = rr.pokazTopCzasy())
    await interaction.response.send_message(embed=embed)
    #Dodać hiperłącza do runów
    #zedytować globalTimes żeby zawierało instanceID


client.run(TOKEN)