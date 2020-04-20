"""
    A discord bot that on request return train departures, travelplan or delays.
    Version: 2020-04-20
"""
import discord
import requests
import json

f = open('Tokens.txt')
lines = f.readlines()
TOKEN = lines[3].strip()
apiKey = lines[4].strip()
apiKey2 = lines[5].strip()
apiKey3 = lines[6].strip()
client = discord.Client()


def avg(id):
    url = "http://api.sl.se/api2/realtimedeparturesv4.json?key=" + apiKey + "&siteid=" + id + "&timewindow=60"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)
    msg = "Tid      Destination \n"
    for i in range(1, 5):
        try:
            msg = msg + (parsed["ResponseData"]["Trains"][i]["DisplayTime"] + "     " +
                         parsed["ResponseData"]["Trains"][i][
                             "Destination"]) + "\n"
        except:
            print("No departure")
    return msg

def resa(id1, id2):

    url = 'https://api.sl.se/api2/TravelplannerV3_1/trip?key=' + apiKey3 + '&originExtId=' + id1 +'&destExtId=' + id2
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)
    msg = ""
    for x in range(3):
        msg = msg + "Alt: " + str(x + 1) + "\n"
        for i in range(0,10):
            try:
                msg = msg + (" -Åk från " + parsed["Trip"][x]["LegList"]["Leg"][i]["Origin"]["name"]
                + " till " + parsed["Trip"][x]["LegList"]["Leg"][i]["Destination"]["name"]
                + " med " + parsed["Trip"][x]["LegList"]["Leg"][i]["Product"]["name"] + " som avgår "
                + parsed["Trip"][x]["LegList"]["Leg"][i]["Origin"]["time"]) + "\n"
            except:
                print("empty")
    return msg

@client.event
async def on_message(message):
    if message.content.startswith('!Hello'):
        msg = 'Hello {0.author.mention}.'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!Help-SL'):
        await message.channel.send(
            "'!Odenplan' \n '!Barkarby' \n '!Jakobsberg' \n '!Kallhäll' \n '!Norrviken' \n '!Sollentuna' \n '!Rudbeck'")

    if message.content.startswith('!Barkarby'):
        await message.channel.send(avg("9703"))

    if message.content.startswith('!Jakobsberg'):
        await message.channel.send(avg("9702"))

    if message.content.startswith('!Kallhäll'):
        await message.channel.send(avg("9701"))

    if message.content.startswith('!Odenplan'):
        await message.channel.send(avg("9117"))

    if message.content.startswith('!Norrviken'):
        await message.channel.send("Stackarn! \n " + avg("9504"))

    if message.content.startswith('!Sollentuna'):
        await message.channel.send(avg("9506"))

    if message.content.startswith('!Rudbeck'):
        await message.channel.send(avg("5514"))

    if message.content.startswith('!Bar-Ode'):
        await message.channel.send("Resa: Barkarby-Odenplan \n" + resa("9703", "9117"))

    if message.content.startswith('!Bar-Rud'):
        await message.channel.send("Resa: Barkarby-Rudbeck \n" + resa("9703", "5514"))

    if message.content.startswith('!Kal-Ode'):
        await message.channel.send("Resa: Kallhäll-Odenplan \n" + resa("9701", "9117"))

    if message.content.startswith("!Delay"):

        url = "http://api.sl.se/api2/deviations.json?key=" + apiKey2 + "&siteId=9117&transportMode=train"
        response = requests.get(url)
        data = response.text
        parsed = json.loads(data)
        msg = "Störningar: \n"
        for i in range(2):
            msg = msg + "•" + parsed["ResponseData"][i]["Header"] + "   " + parsed["ResponseData"][i]["ScopeElements"] + "\n"
        await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')


client.run(TOKEN)
