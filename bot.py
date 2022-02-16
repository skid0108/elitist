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

shadow_bans = []
sweaty = []
mid = []
wysłani = []
wysłani_id = []
poczekalnia = []
tablicaZebyNieWysylaloDwaRazy = []
destroy_channels_3 = []
destroy_channels_2 = []
aplikacje = []

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



@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Pilnowanie Zagubionych", type=4, state="Patrzy"))
    #await update()
    #guild = client.get_guild(847630031659728896)
    #contr_mess_chan = guild.get_channel(847630031659728899)
    #contr_mess = await contr_mess_chan.fetch_message(847645033535766548)
    #await wpisz_w_tablicę(contr_mess.content)
    guild = client.get_guild(567043766108815381)
    role = guild.get_role(943450732621873242)
    while True:
        await role.edit(color=discord.Colour(0xFF0000))
        await asyncio.sleep(2)
        await role.edit(color=discord.Colour(0x000FF0))
        await asyncio.sleep(2)
        await role.edit(color=discord.Colour(0x0FF000))
        await asyncio.sleep(2)




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

        if str(payload.emoji) == "🇻":
            await channel.send(member_ping + " poprosił o szkolenie z VOG-a " + raid_leader)

        await message.remove_reaction(payload.emoji, member)
    
    elif payload.message_id in aplikacje:
        if payload.emoji == "✅":
            await aplikacje[aplikacje.index(payload.message+id) + 1].send("Zostałeś przyjęty na serwer.")
            roless = aplikacje[aplikacje.index(payload.message_id) + 1].roles
            roless.append(guild.get_role(620014821105991680))
            roless.remove(guild.get_role(717327419304050698))
            await aplikacje[aplikacje.index(payload.message_id) + 1].edit(roles=roless)
            aplikacje.remove(aplikacje.index(payload.message_id) + 1)
            aplikacje.remove(aplikacje.index(payload.message_id))
        
        elif payload.emoji == "⛔":
            await aplikacje[aplikacje.index(payload.message_id) + 1].send("Niestety nie zostałeś zaakceptowany na serwer.")
            await aplikacje[aplikacje.index(payload.message_id) + 1].kick()
            aplikacje.remove(aplikacje.index(payload.message_id) + 1)
            aplikacje.remove(aplikacje.index(payload.message_id))

    print(aplikacje)
    print(payload.message_id)



@client.event
async def on_message(message):
    #if not message.guild and message.content.startswith("/turniej"):
        #await message.channel.send("Zapisy do turnieju:\nWybierz dywizję, do której chcesz dołączyć poprzez wpisanie numeru od 1 do 3.:\n1: Sweaty\n2: Mid-sweaty\n3: Kindery")
        #jest = False

        #def check(m):
            #return m.channel == message.channel and m.author == message.author

        #try:
            #msg = await client.wait_for('message', check=check, timeout=15.0)
            #jest = True
        #except asyncio.TimeoutError:
            #await message.channel.send("Za długo, spróbuj ponownie!")

        #if jest:
            #if msg.content == "1" or msg.content == "2" or msg.content == "3":
                #await message.channel.send("Zapisałem Cię do turnieju. Powodzonka!")
                #if msg.content == "1":
                    #global sweaty
                    #sweaty.append(msg.author.id)
                    #await update()

                #elif msg.content == "2":
                    #global mid
                    #mid.append(msg.author.id)
                    #await update()

            #else:
                #await message.channel.send("Wybierz liczbę od 1 do 3! Zacznij od nowa")

    #if not message.guild and message.author.bot == False:
        #if message.attachments:
            #if len(message.attachments) == 1:
                #guild = client.get_guild(847630031659728896)
                #contr_mess_chan = guild.get_channel(847630031659728899)
                #contr_mess = await contr_mess_chan.fetch_message(847645033535766548)

                #if message.author.id not in wysłani_id:
                    #wysłani.append(len(wysłani_id) + 1)
                    #wysłani_id.append(message.author.id)
                    
                    #sklej = ""
                    #x = 0
                    #while x < len(wysłani):
                        #sklej+=f"{wysłani_id[x]} {wysłani[x]}\n"
                        #x+=1
        
                    #await contr_mess.edit(content = sklej)
                    #cont_channel = client.get_channel(847579472043311104)
                    #await cont_channel.send(content = f"Zgłoszenie nr {wysłani[wysłani_id.index(message.author.id)]}:", file = await message.attachments[0].to_file())
                    #await message.channel.send(f"Poprawnie wysłano Twoje zgłoszenie! Twój numer to {wysłani[wysłani_id.index(message.author.id)]}. Powodzenia!")
                #else:
                    #await message.channel.send("Sorry, już się zgłosiłeś!")               
            #else:
                #await message.channel.send("Wyślij tylko jedno zdjęcie!\nSpróbuj ponownie.")
        #else:
            #await message.channel.send("Musisz wysłać jakiś załącznik!\nSpróbuj ponownie.")
            #await message.channel.send("Sorry, zapisy się już skończyły!")
        

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

    elif message.content.upper() == "/DISCORDOWE ID":
        await message.author.send("Twoje ID to " + str(message.author.id))
        await message.delete()

    elif message.attachments:
        if message.channel.id == 789188671584600126 or message.channel.id == 711606924797280348:
            await message.add_reaction("PeepoYes:647938639283879944")
            await message.add_reaction("peepoNo:647938989742882816")
            await message.add_reaction("PvE:798653912075993149")
            await message.add_reaction("PvP:798653320247771188")

    elif message.content == "/help":
            await message.author.send("""Witaj dzielny Strażniku! Oto lista moich funkcji!
        
/awatar [@ktoś] - wyświetla awatar osoby pingowanej, wyświetli Twój jeżeli żaden nie został podany
/discordowe id - wysyła wiadomość prywatną z Twoim discordowym ID

W razie problemów nie bój się napisać do Skid#7847""")
            await message.delete()

    if message.content.upper().startswith("/SEALE"):
        guild = client.get_guild(567043766108815381)
        T = []
        role_id = [810804762894270464, 810804821589622814, 810804840422572043]
        i = 0
        while i < 3:
            T.append(guild.get_role(role_id[i]))
            i+=1

        if len(message.content) == 6:
            seale = discord.Embed(title = f"**Seale: {message.author.display_name}**", color=0xff0000)
            seale.set_author(name = "", icon_url = "https://cdn.discordapp.com/attachments/708605390451114035/810902842729955348/seal.png")

            if T[0] in message.author.roles:
                seale.add_field(name = "**Dungeony**", value = "<:dun_unlocked:824750414545027082>", inline = False)
            else:
                seale.add_field(name = "**~~Dungeony~~**", value = "<:dun_not_unlocked:824755895492673566>", inline = False)

            if T[1] in message.author.roles:
                seale.add_field(name = "**Raidy**", value = "<:raid_unlocked:824741442148106270>",inline = False)
            else:
                seale.add_field(name = "**~~Raidy~~**", value = "<:raid_not_unlocked:824755274362650637>", inline = False)

            if T[2] in message.author.roles:
                seale.add_field(name = "**PvP**", value = "<:pvp_unlocked:824759000553095168>", inline = False)
            else:
                seale.add_field(name = "**~~PvP~~**", value = "<:pvp_not_unlocked:824759000142839888>", inline = False)
            seale.set_thumbnail(url = "https://cdn.discordapp.com/attachments/708605390451114035/810902842729955348/seal.png")

        elif message.mentions:
            odbiorca = message.mentions[0]
            seale = discord.Embed(title = f"**Seale: {odbiorca.display_name}**", color=0xff0000)

            if T[0] in odbiorca.roles:
                seale.add_field(name = "**Dungeony**", value = "<:dun_unlocked:824750414545027082>", inline = False)
            else:
                seale.add_field(name = "**~~Dungeony~~**", value = "<:dun_not_unlocked:824755895492673566>", inline = False)

            if T[1] in odbiorca.roles:
                seale.add_field(name = "**Raidy**", value = "<:raid_unlocked:824741442148106270>",inline = False)
            else:
                seale.add_field(name = "**~~Raidy~~**", value = "<:raid_not_unlocked:824755274362650637>", inline = False)

            if T[2] in odbiorca.roles:
                seale.add_field(name = "**PvP**", value = "<:pvp_unlocked:824759000553095168>", inline = False)
            else:
                seale.add_field(name = "**~~PvP~~**", value = "<:pvp_not_unlocked:824759000142839888>", inline = False)
            seale.set_thumbnail(url = "https://cdn.discordapp.com/attachments/708605390451114035/810902842729955348/seal.png")


        try:
            await message.channel.send(embed = seale)
        except:
            await message.channel.send("Użyj /seale")

    if message.content.upper() == "/WYMAGANIA":
        wymag = discord.Embed(title = f"**Wymagania na seale**", color=0xff0000)
        wymag.add_field(name = "**Dungeony**", value = "Zrobić wszystkie dostępne Dungeony co najmniej solo", inline = False)
        wymag.add_field(name = "**Raidy**", value = "Zrobić wszystkie dostępne raidy, w tym co najmniej dwa flawless", inline = False)
        wymag.add_field(name = "**PvP**", value = "Zrobić Flawlessa na Trialsach lub wbić 5500 Glory", inline = False)
        wymag.set_thumbnail(url = "https://cdn.discordapp.com/attachments/708605390451114035/810902842729955348/seal.png")
        await message.channel.send(embed=wymag)

    if message.content == "jkjk" and message.author.id == 349606518594732055:
        await message.channel.send(".")

    if message.content == "zesrałeś się" and message.author.id == 349606518594732055:
        await update()
        await message.channel.send("no u")

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



@client.event
async def on_member_join(member):
    if member.id in shadow_bans:
        await member.send("Wystąpił błąd! Spróbuj ponownie!")
        await member.kick()

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



    if after.channel and after.channel.id == 901849534332796948: #tworzenie max 3 osobowego i wpisywanie go do tablicy
        nowy_channel = await after.channel.clone(name = "autolobby max 3")
        destroy_channels_3.append(nowy_channel)
        await member.move_to(nowy_channel)

    if after.channel and after.channel.id == 901851165082390548: #tworzenie max 2 osobowego i wpisywanie go do tablicy
        nowy_channel = await after.channel.clone(name = "autolobby max 2")
        destroy_channels_2.append(nowy_channel)
        await member.move_to(nowy_channel)

    if before.channel and len(before.channel.members) == 0: #usuwanie kanału i wywalanie go z listy
        if before.channel in destroy_channels_2 or before.channel in destroy_channels_3:
            await before.channel.delete()
            try:
                destroy_channels_3.remove(before.channel)
            except:
                destroy_channels_2.remove(before.channel)




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
                    aplikacje.append(wiadomosc.id)
                    aplikacje.append(after)
                    print(aplikacje)
                    await wiadomosc.add_reaction("✅")
                    await wiadomosc.add_reaction("⛔")

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

async def update():
    channel = await client.fetch_channel(833466779027111946)
    message = await channel.fetch_message(833468084797964349)
    s = ""
    m = ""
    k = ""
    for x in sweaty:
        s+=f"<@{x}>\n"
    for x in mid:
        m+=f"<@{x}>\n"
    edyt = f"__Sweaty:__\n{s}__Midy:__\n{m}"
    print(edyt)
    await message.edit(content=edyt)
    chanel = await client.fetch_channel(759148536930762783)
    await chanel.send("Zmiana w turnieju. Nowe info to \n" + edyt)


async def wpisz_w_tablicę(string):
    if len(string) > 1:
        for x in string.splitlines():
            wysłani_id.append(int(x.split()[0]))
            wysłani.append(int(x.split()[1]))
        print(wysłani)
        print(wysłani_id)


     



client.run(TOKEN)

