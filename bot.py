import os
import discord
from discord import app_commands
import asyncio
from random import randint
import enums as p
import rr as rr
import hashes as rh
import emblemFinder as EF

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
#ORACLE=None

with open("token.txt") as input:
    try:
        TOKEN = input.read()
    except Exception:
        print("Your token could not be loaded, check you token.txt file")
        

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(name="you fail", type=3))
    await tree.sync(guild=discord.Object(id=968943687272898612))
    #global ORACLE
    #ORACLE = client.get_guild(968943687272898612)
    await rr.initialize(client.guilds)
    await rr.ranksReset(None, True)
    await rr.ticker()
    

def wczytajGildie():
    return client.get_guild(968943687272898612)


@client.event
async def on_message(message):
    if "RATIO" in message.content.upper():
        await message.channel.send(p.ratio[randint(0, len(p.ratio))])

    elif "WE LOSUJ RAIDA" in message.content.upper():
        await message.channel.send("pog, twój raid to...")
        await asyncio.sleep(1)
        await message.channel.send(p.raidyRandom[randint(0, len(p.raidyRandom))])
        
    elif "oPP90" in message.content:
        await message.delete()
        await rr.ranksReset()

@tree.command(name = "leaderboard", description = "Show API speedrun leaderboard", guild=discord.Object(id=968943687272898612))
@app_commands.choices(leaderboard=[app_commands.Choice(name="Global", value="All registered users"), app_commands.Choice(name="Local", value="This server only")])
@app_commands.describe(leaderboard="The type of leaderboard you want to see")
async def leaderboard(interaction, leaderboard: app_commands.Choice[str]):
    await interaction.response.defer(thinking=True)
    rr.wczytaj()
    rr.request_data()
    embed = discord.Embed(title = f"{leaderboard.name} raid times", color = 0x000000)
    embed.set_footer(text="Brought to you by Elitist",icon_url="https://www.bungie.net/common/destiny2_content/icons/3c251b702026fee24488eac5cbd3a2e2.jpg")
    if leaderboard.name == "Global":
        embed.add_field(name = "Click on the times for RR page",value = await rr.print_speedrun_leaderboard())
    elif leaderboard.name == "Local":
        embed.add_field(name = "Click on the times for RR page",value = await rr.print_speedrun_leaderboard(interaction.guild))
    await interaction.followup.send(embed=embed)


@tree.command(name = "link", description = "link your Discord account with your bungie.net", guild=discord.Object(id=968943687272898612))
async def register(interaction):
    embed = discord.Embed(title = "Linking accounts", color = 0x000000, )
    embed.set_footer(text="Brought to you by Elitist",icon_url="https://www.bungie.net/common/destiny2_content/icons/3c251b702026fee24488eac5cbd3a2e2.jpg")
    embed.add_field(name='You only need to do this once', value=f"[Click here to register!](https://93.181.133.46:8000/?discord_id={interaction.user.id})")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    #response = await rr.dodajKonto(tag, interaction.user.id)


@tree.command(name = "emblem", description = "Search for emblem stats", guild=discord.Object(id=968943687272898612))
async def getEmblem(interaction, emblem: str):
    await interaction.response.defer(thinking=True)
    emlemInfo = EF.emblem_search(emblem)
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
    #rr.best_times(rr.registered_accounts)
    await interaction.followup.send(embed=await rr.ranksReset(interaction.guild, True))


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


@tree.command(name = "grade", description = "Grades your achievements and gives you reccomendations on what to do next!", guild=discord.Object(id=968943687272898612))
async def achievements(interaction):
    embed = discord.Embed(title = "Your overall grade", color = 0x000000, )
    embed.set_footer(text="Brought to you by Elitist",icon_url="https://www.bungie.net/common/destiny2_content/icons/3c251b702026fee24488eac5cbd3a2e2.jpg")
    val = rr.overall_grade(interaction.user.id)
    embed.add_field(name='Your grade is:', value=f'{val[0]}', inline=False)
    wtd = ''.join([f'{x[0]}: {rh.frontendNames[x[1]]}\n' for x in val[1]])
    embed.add_field(name='What should you focus on:', value=wtd, inline=False)
    
    await interaction.response.send_message(embed=embed)


client.run(TOKEN)
