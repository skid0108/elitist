import os
import discord
from discord import app_commands
import asyncio
from random import randint
import enums as p
import rr as rr
import emblemFinder as EF

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
ORACLE=None
TOKEN = "YOUR TOKEN HERE"
        

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(name="you fail", type=3))
    await tree.sync(guild=discord.Object(id=968943687272898612))
    global ORACLE
    ORACLE = client.get_guild(968943687272898612)
    rr.initialize([ORACLE])
    await rr.ranksReset(None, True)
    await rr.ticker()
    

def wczytajGildie():
    return client.get_guild(968943687272898612)


@client.event
async def on_message(message):
    if "RATIO" in message.content.upper():
        await message.channel.send(p.ratio[randint(len(p.ratio))])

    elif "WE LOSUJ RAIDA" in message.content.upper():
        await message.channel.send("pog, twój raid to...")
        await asyncio.sleep(1)
        await message.channel.send(p.raidyRandom[randint(len(p.raidyRandom))])
    

@tree.command(name = "leaderboard", description = "Show API speedrun leaderboard", guild=discord.Object(id=968943687272898612))
@app_commands.choices(leaderboard=[
        app_commands.Choice(name="Global", value="All registered users"),
        app_commands.Choice(name="Local", value="This server only")])
@app_commands.describe(leaderboard="The type of leaderboard you want to see")
async def leaderboard(interaction, leaderboard: app_commands.Choice[str]):
    await interaction.response.defer(thinking=True)
    embed = discord.Embed(title = f"{leaderboard.name} raid times", color = 0x000000)
    embed.set_footer(text="Brought to you by Elitist",icon_url="https://www.bungie.net/common/destiny2_content/icons/3c251b702026fee24488eac5cbd3a2e2.jpg")
    if leaderboard.name == "Global":
        embed.add_field(name = "Click on the times for RR page",value = await rr.pokazTopCzasy())
    elif leaderboard.name == "Local":
        embed.add_field(name = "Click on the times for RR page",value = await rr.pokazTopCzasy(interaction.guild))
    await interaction.followup.send(embed=embed)


@tree.command(name = "register", description = "link your Discord account with your bungie.net", guild=discord.Object(id=968943687272898612))
@app_commands.describe(tag="Your bungie.net tag")
async def register(interaction, tag: str):
    await interaction.response.send_message(await rr.dodajKonto(tag, interaction.user.id))
    await rr.rozdajRangi()
    await rr.updateCzasy()


@tree.command(name = "emblem", description = "Search for emblem stats", guild=discord.Object(id=968943687272898612))
async def getEmblem(interaction, emblem: str):
    await interaction.response.defer(thinking=True)
    emlemInfo = EF.emblem_search(emblem)
    print(emlemInfo)
    if isinstance(emlemInfo, str):
        await interaction.followup.send(emlemInfo)
        return
    else:
        embed = discord.Embed(title = emlemInfo[0][0], color = 0x000000)
        embed.set_footer(text="Brought to you by Destinuś",icon_url="https://www.bungie.net/common/destiny2_content/icons/3c251b702026fee24488eac5cbd3a2e2.jpg")
        for x in range(1, len(emlemInfo[0])):
            lines = emlemInfo[0][x].split(":")
            embed.add_field(name = lines[0],value = lines[1], inline=False)
            embed.set_thumbnail(url=emlemInfo[1])
    await interaction.followup.send(embed=embed)


@tree.command(name = "clears", description = "Show clear leaderboard for given timeframe", guild=discord.Object(id=968943687272898612))
@app_commands.choices(leaderboard=[
        app_commands.Choice(name="Weekly", value="Weekly")])
@app_commands.describe(leaderboard="Timeframe")
async def clears(interaction, leaderboard: app_commands.Choice[str]):
    await interaction.response.defer(thinking=True)
    rr.getCzasy(rr.zarejestrowaneKonta)
    await interaction.followup.send(embed=await rr.ranksReset(None, True))


@tree.command(name = "add", description = "Add this channel to enable certain functions", guild=discord.Object(id=968943687272898612))
@app_commands.choices(leaderboard=[
        app_commands.Choice(name="Weekly clears", value="Weekly clears"),
        app_commands.Choice(name="Speedrun roles", value="Speedrun roles")])
@app_commands.describe(leaderboard="Functions you want to be added for this channel")
async def clears(interaction, leaderboard: app_commands.Choice[str]):
    await interaction.response.defer(thinking=True)
    if leaderboard.name == "Weekly clears":
        rr.add(1, interaction.channel.id)
    elif leaderboard.name == "Speedrun roles":
        rr.add(0, interaction.guild.id)
    await interaction.followup.send(f"Channel added to {leaderboard.name}")



client.run(TOKEN)
