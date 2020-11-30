import os
import discord


TOKEN = 'NzE5MjY1MzgyMTI0MjI0NjA0.Xt0_zg.26lDdEyu_WXpTOGDbKrN8Gr7OjE'
client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Napisz, aby coś zgłosić!"))


@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 722816539061125171:
        guild = discord.utils.find(
            lambda g: g.id == payload.guild_id, client.guilds)

        raid_leader = '<@&645191000041586719>'

        channel = discord.utils.get(guild.text_channels, name='szkolenia')
        origin_channel = discord.utils.get(
            guild.text_channels, name='chcę-szkolenia')

        message = await origin_channel.fetch_message(722816539061125171)
        member = await guild.fetch_member(payload.user_id)
        member_ping = '<@' + str(payload.user_id) + '>'

        #if str(payload.emoji) == u"\U0001F1F1":
            #await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Leviathan ' + raid_leader)

        #if str(payload.emoji) == u"\U0001F1EA":
            #await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Eater of Worlds ' + raid_leader)

        #if str(payload.emoji) == u"\U0001F1F8":
            #await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Spire of Stars ' + raid_leader)

        #if str(payload.emoji) == u"\U0001F1F0":
            #await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Crown of Sorrow ' + raid_leader)

        #if str(payload.emoji) == u"\U0001F1E7":
            #await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Scourge of the Past ' + raid_leader)

        if str(payload.emoji) == u"\U0001F1FC":
            await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Last Wish ' + raid_leader)

        if str(payload.emoji) == u"\U0001F1EC":
            await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Garden of Salvation ' + raid_leader)

        if str(payload.emoji) == "🇩":
            await channel.send(member_ping + " poprosił o szkolenie z DSC " + raid_leader)

        await message.remove_reaction(payload.emoji, member)


@client.event
async def on_message(message):
    if not message.guild:
        if not message.author.bot:
            await message.channel.send("""Dzięki za zgłoszenie!
Zostało ono przekazane do teamu i będzie rozpatrzone w niedalekiej przyszłości.
""")
            kanal = client.get_channel(759148536930762783)
            member_ping = '<@' + str(message.author.id) + '>'
            await kanal.send(member_ping + """ 
""" + message.content + '\n-------------------------------')

    elif "Przyzywam" in message.content and message.author.id == 349606518594732055:
        guild = client.get_guild(567043766108815381)
        member_id = message.content[10:28]
        ilosc = message.content[29:]
        member = await guild.fetch_member(member_id)
        x = 0
        await message.add_reaction("PeepoYes:647938639283879944")
        while x < int(ilosc):
            await member.send("KTOŚ CIĘ WZYYYYYYYWA")
            x +=1
        await message.channel.send(str(member) + " został przyzwany " + str(x) + " razy <:Pepega:590993310055792640>")
    
    elif "AWATAR" in message.content.upper():
        if len(message.content) == 6:
            member = message.author
        else:
            guild = client.get_guild(567043766108815381)
            member_id = message.content[7:]
            member = await guild.fetch_member(member_id)
        
        await message.channel.send(str(member.avatar_url))
        await message.delete()

    elif message.content.upper() == "DISCORDOWE ID":
        await message.author.send("Twoje ID to " + str(message.author.id))
        await message.delete()

    elif message.attachments and message.channel.id == 711606924797280348:
        await message.add_reaction("PeepoYes:647938639283879944")
        await message.add_reaction("peepoNo:647938989742882816")
        
    



client.run(TOKEN)



