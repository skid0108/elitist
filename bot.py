import os
import discord

TOKEN = "NzkxMzE2MjAyOTc0MjE2MjQy.X-NYpA.hYCliU9r1uKyFI7jlYOEzHPyN-o"
intents = discord.Intents.all()
client = discord.Client(intents=intents)

shadow_bans = [226395472410050561, 622725935992406037]


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Pilnowanie Zagubionych", type=4, state="Patrzy"))


@client.event
async def on_raw_reaction_add(payload):
    guild = client.get_guild(567043766108815381)
    kanal = guild.get_channel(628647068436660255)
    orkanal = guild.get_channel(569992958368284694)
    wiad = await orkanal.fetch_message(710990524571713607)
    user = await guild.fetch_member(payload.user_id)
    if payload.message_id == wiad.id:
        if payload.emoji.name == "PeepoBeers":
            if user.top_role == guild.get_role(626144153864110090):
                await user.add_roles(guild.get_role(628637262430863381))
                await kanal.send("""<@&609074752211910668> <@&665635028872724481> <@&590871493001609226>
Pojawił się nowy rekrut, """ + user.mention + "!")
                await wiad.remove_reaction(payload.emoji, user)
            else:
                await user.send("Sorka, ale nie możesz nadać sobie tej roli. Napisz do administracji, dzięki!")
                await wiad.remove_reaction(payload.emoji, user)

    elif payload.message_id == 722816539061125171:
        print("henlo")

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
    if not message.guild and message.content.startswith("/zgłaszam"):
       	await message.channel.send("""Dzięki za zgłoszenie!
Zostało ono przekazane do teamu i będzie rozpatrzone w niedalekiej przyszłości.
""")
       	kanal = client.get_channel(759148536930762783)
       	member_ping = '<@' + str(message.author.id) + '>'
       	await kanal.send(member_ping + """ 
""" + message.content[10:] + '\n-------------------------------')

    elif "Przyzywam" in message.content and message.author.id == 349606518594732055:
        guild = client.get_guild(567043766108815381)
        skid = await guild.fetch_member(349606518594732055)
        skidchannel = skid.voice.channel
        kanal = await skidchannel.create_invite(max_age = 300, max_users = 1)
        member_id = message.mentions[0].id
        member = await guild.fetch_member(member_id)
        x = 0
        await message.add_reaction("PeepoYes:647938639283879944")
        while x < 4:
            await member.send("Skid Cię potrzebuje! Odpowiesz na wezwanie?")
            x +=1
        await member.send(kanal)
        await message.channel.send(str(member) + " został przyzwany <:Pepega:590993310055792640>")
    
    elif "/AWATAR" in message.content.upper():
        if len(message.content) == 7:
            member = message.author
        else:
            guild = client.get_guild(567043766108815381)
            member_id = message.mentions[0].id
            member = await guild.fetch_member(member_id)
        
        await message.channel.send(str(member.avatar_url))
        await message.delete()

    elif message.content.upper() == "/DISCORDOWE ID":
        await message.author.send("Twoje ID to " + str(message.author.id))
        await message.delete()

    elif message.attachments:
        if message.channel.id == 789188671584600126 or message.channel.id == 711606924797280348:
        	await message.add_reaction("PeepoYes:647938639283879944")
        	await message.add_reaction("peepoNo:647938989742882816")

    elif message.content == "/help":
            await message.author.send("""Witaj dzielny Strażniku! Oto lista moich funkcji!
        
/awatar [@ktoś] - wyświetla awatar osoby pingowanej, wyświetli Twój jeżeli żaden nie został podany
/discordowe id - wysyła wiadomość prywatną z Twoim discordowym ID

W razie problemów nie bój się napisać do Skid#7847""")
            await message.delete()


    if message.guild.id == 742679443071565916 and message.content == "restart":
        liczba = 0
        guild = message.guild
        anchor = guild.get_role(743001990317211689)
        for x in guild.members:
            if anchor in x.roles:
                await x.remove_roles(anchor, reason="Restart")
                liczba += 1
        await message.channel.send(f"Usunięto rolę 'Anchor' z {liczba} członków" )



@client.event
async def on_member_join(member):
    if member.id in shadow_bans:
        await member.send("Wystąpił błąd! Spróbuj ponownie!")
        await member.kick()


client.run(TOKEN)



