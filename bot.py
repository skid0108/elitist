import os
import discord
from discord import Colour
import asyncio
from random import randint

from discord import channel
from discord.gateway import EventListener

TOKEN = "NzkxMzE2MjAyOTc0MjE2MjQy.X-NYpA.hYCliU9r1uKyFI7jlYOEzHPyN-o"
intents = discord.Intents.all()
client = discord.Client(intents=intents)

poczekalnia = []
tablicaZebyNieWysylaloDwaRazy = []
destroy_channels_3 = []
destroy_channels_2 = []
destroy_channels_4 = []
destroy_channels_6 = []
destroy_channels_lim = []
aplikacje = []
aplikacjeLudzie = []

raidy = {
    4: "VoG",
    3: "DSC",
    2: "GoS",
    1: "LW"
}

opcje = {
    "JAKIEGOKOLWIEK": 4,
    "NIENUDNEGO": 3,
    "FAJNEGO": 2,
    "NAJLEPSZEGO": 1
}

ratio = {
    1: "https://media.giphy.com/media/JONVSqlDvbKfrkK1ys/giphy.gif",
    2: "https://tenor.com/view/trump-donaldtrump-interview-banned-cnn-gif-7677105",
    3: "https://imgur.com/jIxteBQ",
    4: "https://gfycat.com/simpledeliriousasianporcupine",
    5: "https://media.discordapp.net/attachments/798363780714856500/921838687795429376/jameswerk.gif",
    6: "https://media.discordapp.net/attachments/813334484039630910/941355773764730921/ezgif.com-gif-maker_23.gif",
    7: "https://gfycat.com/biodegradablegrosskoi",
    8: "https://media.giphy.com/media/pvXPiREYPUSTo4fbBv/giphy-downsized-large.gif",
    9: "https://media4.giphy.com/media/fUp4znpeoWm4HgPwre/giphy.mp4?cid=73b8f7b170a931f372b250157974124fc308656ba1eb7e83&rid=giphy.mp4&ct=g",
    10: "https://media.giphy.com/media/oop0T7d8GhfgbxMYd9/giphy.gif",
    11: "https://media.discordapp.net/attachments/827552926360272936/910167807126306916/ratio1.gif",
    12: "https://tenor.com/view/trump-donaldtrump-interview-banned-cnn-gif-7677105",
    13: "https://media.discordapp.net/attachments/922000064262574110/926049849739190272/8C43B7B9-DA30-4E91-9F28-43C3092D78BE-1280-000000C28D43E321.gif",
    14: "https://media.giphy.com/media/P4R5fySS7gl0nS5t7H/giphy.gif",
    15: "https://media.discordapp.net/attachments/827552926360272936/910167807126306916/ratio1.gif",
    16: "https://media.discordapp.net/attachments/484153257753837568/913226774329065552/vog_ratio.gif",
    17: "https://gfycat.com/caringgloomyhalicore",
    18: "https://media.giphy.com/media/9YX4P3CFrXsTNBCPAQ/giphy.gif",
    19: "https://media.discordapp.net/attachments/809286191538896966/899145578561302548/ratiorakka.gif",
    20: "https://imgur.com/a/itiUO4Q",
    21: "https://gfycat.com/wanaggressiveivorybackedwoodswallow",
}



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
                await kanal.send("""<@&655170106711736330>
Pojawił się nowy rekrut, """ + user.mention + "!")
                await wiad.remove_reaction(payload.emoji, user)
            else:
                await user.send("Sorka, ale nie możesz nadać sobie tej roli. Napisz do administracji, dzięki!")
                await wiad.remove_reaction(payload.emoji, user)

    
    if payload.message_id in aplikacje and not payload.member.bot:
        print(payload.emoji.id)
        print(payload.emoji.name)
        if payload.emoji.name == "PeepoYes":
            dest = aplikacjeLudzie[aplikacje.index(payload.message_id)]
            await dest.send("Zostałeś przyjęty na serwer!")
            roless = aplikacjeLudzie[aplikacje.index(payload.message_id)].roles
            roless.append(guild.get_role(620014821105991680))
            roless.remove(guild.get_role(717327419304050698))
            await aplikacjeLudzie[aplikacje.index(payload.message_id)].edit(roles=roless)
            aplikacje.remove(payload.message_id)
            aplikacjeLudzie.remove(dest)
        
        elif payload.emoji.name == "peepoNo":
            dest = aplikacjeLudzie[aplikacje.index(payload.message_id)]
            await aplikacjeLudzie[aplikacje.index(payload.message_id)].send("Niestety nie zostałeś zaakceptowany na serwer.")
            await aplikacjeLudzie[aplikacje.index(payload.message_id)].kick()
            aplikacje.remove(payload.message_id)
            aplikacjeLudzie.remove(dest)



@client.event
async def on_message(message):
    if "RATIO" in message.content.upper():
        await message.channel.send(ratio[randint(1, 21)])

    if "!SNIPE" in message.content.upper():
        target = await client.get_guild(567043766108815381).fetch_member(message.content[7:])
        print(message.content[7:])
        print(target)
        target_channel = client.get_channel(567061405346299904)
        for i in range(0, 3):
            await asyncio.sleep(15)
            await target.move_to(target_channel)


    if message.content == "rgbjk":
        await message.channel.send("ok")
        guild = client.get_guild(567043766108815381)
        role = guild.get_role(943450732621873242)
        colours = [0xFF0000, 0x00FF00, 0x0000FF]
        i = 0

        while True:
            await asyncio.sleep(5)
            i = (i + 1) % 3
            print("Color changed")
            await role.edit(colour=discord.Colour(colours[i]))        

    if "Przyzywam" in message.content and message.author.id == 349606518594732055:
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

    elif message.attachments:
        if message.channel.id == 789188671584600126 or message.channel.id == 711606924797280348:
            await message.add_reaction("PeepoYes:647938639283879944")
            await message.add_reaction("peepoNo:647938989742882816")
            await message.add_reaction("PvE:798653912075993149")
            await message.add_reaction("PvP:798653320247771188")

    elif message.content == "jkjk" and message.author.id == 349606518594732055:
        await message.channel.send(".")

    elif message.content.upper() == "WE LOSUJ RAIDA":
            await message.channel.send('__jakiego raida chcesz byq?__\n*jakiegokolwiek\n*nienudnego\n*fajnego\n*najlepszego')

            def check(m):
                return m.channel == message.channel and m.author == message.author

            try:
                msg = await client.wait_for('message', check=check, timeout=45)
                if msg.content.upper() in ["JAKIEGOKOLWIEK", "NIENUDNEGO", "FAJNEGO", "NAJLEPSZEGO"]:
                    await message.channel.send("pog, twój raid to...")
                    await asyncio.sleep(1)
                    await message.channel.send(raidy[randint(1, opcje[msg.content.upper()])])
                else:
                    await message.channel.send("Zyebaueś")
            except asyncio.TimeoutError:
                await message.channel.send("Zyebaueś")

    elif "WESPINGUJ" in message.content.upper() and message.author.id == 349606518594732055:
        role = message.role_mentions[0]
        guild = message.guild
        msg = ''
        xd = 1
        for x in  guild.members:
            if role in x.roles:
                msg += (f"{xd}. <@{x.id}>\n")
                xd+=1
        await message.channel.send(msg)


@client.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id == 813399282773262347:
        if str(member.display_name) not in  poczekalnia:
            poczekalnia.append(str(member.display_name))
            await edytuj()

    if before.channel and before.channel.id == 813399282773262347:
        await asyncio.sleep(300)
        if not member.voice or member.voice and member.voice.channel != before.channel:
            poczekalnia.remove(str(member.display_name))
            await edytuj()

    if after.channel and after.channel.id == 767769111530176562: #tworzenie max 2 osobowego i wpisywanie go do tablicy [ZS]
        nowy_channel = await after.channel.clone(name = "Max 2")
        await nowy_channel.move(end=True, offset=-1)
        destroy_channels_2.append(nowy_channel)
        await member.move_to(nowy_channel)

    if after.channel and after.channel.id == 775642427335114753: #tworzenie max 3 osobowego i wpisywanie go do tablicy [ZS]
        nowy_channel = await after.channel.clone(name = "Max 3")
        await nowy_channel.move(end=True, offset=-1)
        destroy_channels_3.append(nowy_channel)
        await member.move_to(nowy_channel)

    if after.channel and after.channel.id == 775642033410408448: #tworzenie max 4 osobowego i wpisywanie go do tablicy [ZS]
        nowy_channel = await after.channel.clone(name = "Max 4")
        await nowy_channel.move(end=True, offset=-1)
        destroy_channels_4.append(nowy_channel)
        await member.move_to(nowy_channel)

    if after.channel and after.channel.id == 567061405346299904: #tworzenie max 6 osobowego i wpisywanie go do tablicy [ZS]
        nowy_channel = await after.channel.clone(name = "Max 6")
        await nowy_channel.move(end=True, offset=-1)
        destroy_channels_6.append(nowy_channel)
        await member.move_to(nowy_channel)

    if after.channel and after.channel.id == 567061439659900948: #tworzenie limitless i wpisywanie go do tablicy [ZS]
        nowy_channel = await after.channel.clone(name = "Limitless")
        await nowy_channel.move(end=True, offset=-1)
        destroy_channels_lim.append(nowy_channel)
        await member.move_to(nowy_channel)

    if after.channel and after.channel.id == 901849534332796948: #tworzenie max 3 osobowego i wpisywanie go do tablicy
        nowy_channel = await after.channel.clone(name = "autolobby max 3")
        destroy_channels_3.append(nowy_channel)
        await member.move_to(nowy_channel)

    if after.channel and after.channel.id == 901851165082390548: #tworzenie max 2 osobowego i wpisywanie go do tablicy
        nowy_channel = await after.channel.clone(name = "autolobby max 2")
        destroy_channels_2.append(nowy_channel)
        await member.move_to(nowy_channel)

    if member.id == 366253807837118474:
        await member.move_to(None, reason="Error 403 - contact support")



    if before.channel and len(before.channel.members) == 0: #usuwanie kanału i wywalanie go z listy
        if before.channel in destroy_channels_2:
            await before.channel.delete()
            destroy_channels_2.remove(before.channel)
        if before.channel in destroy_channels_3:
            await before.channel.delete()
            destroy_channels_3.remove(before.channel)
        if before.channel in destroy_channels_4:
            await before.channel.delete()
            destroy_channels_4.remove(before.channel)
        if before.channel in destroy_channels_6:
            await before.channel.delete()
            destroy_channels_6.remove(before.channel)
        if before.channel in destroy_channels_lim:
            await before.channel.delete()
            destroy_channels_lim.remove(before.channel)


    if after.channel:
        if after.channel in destroy_channels_3 and after.channel != before.channel:
            if len(after.channel.members) > 3:
                await member.edit(mute=True)
            else:
                await asyncio.sleep(2)
                await member.edit(mute=False)
        elif after.channel.id == 901142385390657546:
            await asyncio.sleep(2)
            await member.edit(mute=False)

    if after.channel:
        if after.channel in destroy_channels_2 and after.channel != before.channel:
            if len(after.channel.members) > 2:
                await member.edit(mute=True)
            else:
                await asyncio.sleep(2)
                await member.edit(mute=False)
        elif after.channel.id == 901142385390657546:
            await asyncio.sleep(2)
            await member.edit(mute=False)


@client.event
async def on_member_update(before, after):
    guild = client.get_guild(567043766108815381)
    tamtoId = guild.get_role(717327419304050698)
    if tamtoId in after.roles and after not in tablicaZebyNieWysylaloDwaRazy:
        tablicaZebyNieWysylaloDwaRazy.append(after)
        await after.send("Siema, zanim dodamy Cię do naszego serwera mamy trzy pytania.")
        await after.send("1/3. Z jakiego klanu jesteś?")

        def check(m):
            return m.channel == after.dm_channel and m.author == after

        try:
            msg = await client.wait_for('message', check=check, timeout=28800.0)
            klan = msg
            await after.send("2/3. W jakim celu chcesz dołączyć do nas jako gość?")

            try:
                msg = await client.wait_for('message', check = check, timeout = 28800.0)
                dlaczego = msg
                await after.send("3/3. Wypisz nicki osób, które znasz lub z którymi grałeś, należących do naszego klanu.")

                try:
                    msg = await client.wait_for('message', check = check, timeout = 28800.0)
                    poreczyciel = msg
                    await after.send("Okej, dziena za odpowiedź. Zaraz ktoś się Tobą zajmie, o ile ktoś jest aktywny.")
                    embed = discord.Embed(title = f"**Zgłoszenie nowego invadera - {after.name}**", color=0xff0000)
                    embed.add_field(name = "**Klan**", value = klan.content, inline = False)
                    embed.add_field(name = "**Dlaczego chce dołączyć**", value = dlaczego.content, inline = False)
                    embed.add_field(name = "**Znane osoby**", value = poreczyciel.content, inline = False)
                    embed.set_thumbnail(url = after.avatar_url)
                    wiadomosc = await guild.get_channel(590242444633964557).send(embed=embed)
                    print(wiadomosc.id)
                    aplikacje.append(wiadomosc.id)
                    aplikacjeLudzie.append(after)
                    await wiadomosc.add_reaction(":PeepoYes:647938639283879944")
                    await wiadomosc.add_reaction(":peepoNo:647938989742882816")

                except asyncio.TimeoutError:
                    await after.send("Twój czas na odpowiedź minął.")
                    await guild.get_channel(590242444633964557).send(f"{after.name} nie wprowadził danych do formularza, do wyjebania.")

            except asyncio.TimeoutError:
                await after.send("Twój czas na odpowiedź minął.")
                await guild.get_channel(590242444633964557).send(f"{after.name} nie wprowadził danych do formularza, do wyjebania.")

        except asyncio.TimeoutError:
            await after.send("Twój czas na odpowiedź minął.")
            await guild.get_channel(590242444633964557).send(f"{after.name} nie wprowadził danych do formularza, do wyjebania.")
 

async def edytuj():
    channel = await client.fetch_channel(822898782894161930)
    message = await channel.fetch_message(822899080921350154)
    print(poczekalnia)
    c = len(poczekalnia)
    if c > 0:
        if c == 1:
            ss = f"""```1: {poczekalnia[0]}\n2:\n3:\n4:\n5:\n```"""
        elif c == 2:
            ss = f"""```1: {poczekalnia[0]}\n2: {poczekalnia[1]}\n3:\n4:\n5:\n```"""
        elif c == 3:
            ss = f"""```1: {poczekalnia[0]}\n2: {poczekalnia[1]}\n3: {poczekalnia[2]}\n4:\n5:\n```"""
        elif c == 4:
            ss = f"""```1: {poczekalnia[0]}\n2: {poczekalnia[1]}\n3: {poczekalnia[2]}\n4: {poczekalnia[3]}\n5:\n```"""
        elif c >= 5:
            ss = f"""```1: {poczekalnia[0]}\n2: {poczekalnia[1]}\n3: {poczekalnia[2]}\n4: {poczekalnia[3]}\n5: {poczekalnia[4]}```"""
    else:
        ss = "```Kolejka jest pusta```"
    await message.edit(content=ss)  


client.run(TOKEN)

