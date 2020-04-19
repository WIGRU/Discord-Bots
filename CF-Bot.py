"""
This program is a discord bot that present different scores from Catching features
Authors: William Grunder & Oskar Edvardsson
Version: 2020-04-17
"""
import discord
import requests
from bs4 import BeautifulSoup
import re

# Gets discord token from text file Tokens.txt
f = open('Tokens.txt')
lines = f.readlines()
TOKEN = lines[0]

client = discord.Client()

# Club and runners that will be searched after
club = "Järfälla OK"
names = ["OskarEdvardsson", "erbo", "Jesper Åkesson", "Willis"]


# Get page content using requests and bs4
def pageReq(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


@client.event
async def on_message(message):
    # The bot is not supposed to answer its own messages.
    if message.author == client.user:
        return

    if message.content.startswith('!Hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!Help'):
        msg = "Commands \n '!Score' \n '!Rank' - Ranks in JOK\n '!Servers' - Servers online \n '!Calender' \n " \
              "'!WC-Rank' - Club wc ranking \n '!WC' - Personal ranking wc"
        await message.channel.send(msg)

    # Get ranking-score with usernames.
    if message.content == '!Score':
        soup = pageReq('http://www.catchingfeatures.com/clubinfo.php?c=J%C3%A4rf%C3%A4lla+OK')

        msg = "Namn    Poäng \n"
        msg = msg + "-------------------- \n"
        for i in range(len(names)):
            t = soup.find(text=names[i])
            t = t.findParent().findParent().findParent()
            t = t.findAll('td')
            msg = msg + (names[i] + ": " + t[len(t) - 2].text + "\n")
        await message.channel.send(msg)

    # Get rank and score of all players in club.
    if message.content == '!Rank':
        soup = pageReq('http://catchingfeatures.com/comps/rankings.php')

        tList = soup.findAll(text=club)

        msg = "Plc.  Namn    Poäng \n"
        for i in range(len(tList)):
            print(tList[i])
        for i in range(len(tList)):
            t = tList[i].findParent().findParent().findParent()
            t = t.findAll('td')
            try:
                msg = msg + (t[0].text + " " + t[1].text + " " + t[4].text + "\n")
            except:
                print("e: t didn't have enough values")
        await message.channel.send(msg)

    # Returns all servers that is online.
    if message.content == '!Servers':
        soup = pageReq('http://catchingfeatures.com/multi.php')

        t = soup.find(text="Server Name")
        t = t.findParent().findParent().findParent()
        t = t.findAll('td')
        msg = "Name                              Status \n"
        msg = msg + "------------------------------------\n"
        try:
            for i in range(1, len(t) // 4):
                msg = msg + (t[i * 5 - 1].text[:15].strip() + "      " + t[i * 5 + 2].text.strip() + "\n")
            await message.channel.send(msg)
        except:
            await message.channel.send("No servers online :(")

    # Returns world cup club-ranking.
    if message.content == '!WC-Rank':
        soup = pageReq('http://catchingfeatures.com/comps/series2.php?s=666')

        t = soup.find(text=re.compile(".*" + club + ".*"))
        t = t.findParent().findParent()
        t = t.findAll('td')
        msg = t[0].text + "\n"
        st = 0
        for i in range(1, len(t) - 1):
            msg = msg + "Etapp " + str(i) + ": " + t[i].text + "\n"
        msg = msg + "Totalt: " + t[len(t) - 1].text + "\n"

        await message.channel.send(msg)

    # Returns world cup ranking.
    if message.content == '!WC':
        soup = pageReq('http://www.catchingfeatures.com/comps/series.php?s=666')
        msg = "plc.    Namn \n"
        msg = msg + "-------------------- \n"
        for i in range(len(names)):
            t = soup.find(text=names[i])
            t = t.findParent().findParent().findParent()
            t = t.findAll('td')
            msg = msg + t[0].text + "\n"
        await message.channel.send(msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')


client.run(TOKEN)
