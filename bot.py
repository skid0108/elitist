import os
import discord


TOKEN = 'NzE5MjY1MzgyMTI0MjI0NjA0.Xt0_zg.26lDdEyu_WXpTOGDbKrN8Gr7OjE'
client = discord.Client()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="v1.0.1"))


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
        member = guild.get_member(payload.user_id)
        member_ping = '<@' + str(payload.user_id) + '>'

        if str(payload.emoji) == u"\U0001F1F1":
            await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Leviathan ' + raid_leader)

        if str(payload.emoji) == u"\U0001F1EA":
            await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Eater of Worlds ' + raid_leader)

        if str(payload.emoji) == u"\U0001F1F8":
            await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Spire of Stars ' + raid_leader)

        if str(payload.emoji) == u"\U0001F1F0":
            await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Crown of Sorrow ' + raid_leader)

        if str(payload.emoji) == u"\U0001F1E7":
            await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Scourge of the Past ' + raid_leader)

        if str(payload.emoji) == u"\U0001F1FC":
            await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Last Wish ' + raid_leader)

        if str(payload.emoji) == u"\U0001F1EC":
            await channel.send(member_ping + ' poprosił o szkolenie z ' + 'Garden of Salvation ' + raid_leader)

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
    if message.author.id == 330384207106932736 and message.guild:
        await message.add_reaction("Jerry:649266456080678943")

client.run(TOKEN)
