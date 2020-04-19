"""
    This is a bot to fast access info conected to orienteering.
    Version: 2020-04-19
"""
import discord
import requests
from bs4 import BeautifulSoup
import datetime
import feedparser
import xml.etree.ElementTree as ET
import logging

# get discord token and eventor api key that is stored in a textfile
# called "Tokens.txt". line 0 = discord token line 1 = eventor key
f = open('Tokens.txt')
lines = f.readlines()
TOKEN = lines[0]
EVENTOR_KEY = lines[1]

client = discord.Client()

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# Get page content using requests and bs4
def pageReq(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


@client.event
async def on_message(message):

    def log(text):
        print(str(datetime.datetime.now()) + ": {0.author.mention} ".format(message) + text)

    # The bot is not supposed to answer its own messages
    if message.author == client.user:
        return

    if message.content.startswith('!Hello'):
        msg = 'Hello {0.author.mention}. Write !Help to get list of commands.'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!Help'):
        msg = "Commands \n '!Calender' - Calender for the next 7 days \n '!News' - Shows the latest news \n" \
              "'!SO-News' - Latest news from SOFT \n '!Comp' - Todays competitions from eventor"
        await message.channel.send(msg)

    # Shows calender activities for the next seven days from www.jarfallaok.se
    if message.content == "!Calender":
        dt = datetime.datetime.today()
        soup = pageReq('https://www.jarfallaok.se/kalender/index.php#dt')
        msg = ""
        for i in range(7):
            try:
                day = "d" + str(dt.day + i)
                t = soup.find(id=day)
                t = t.findAll('td')
                msg = msg + (t[0].text + t[1].text + "\n")
            except:
                log("e: couldn't find day")
        await message.channel.send(msg)

    # Shows the latest news from JOK
    if message.content == "!News":
        dt = datetime.datetime.today()
        soup = pageReq('https://www.jarfallaok.se/nyhet.php?x=list&a=' + str(dt.year))
        msg = "Latest new \n ---------------"
        t = soup.find(id="jok-news-row")
        t = t.findAll('h3')
        t.reverse()
        for i in range(3):
            print(t[i].text)
            msg = msg + "-" + t[i].text
        await message.channel.send(msg)

    # Latest news from SOFT
    if message.content == "!SO-News":
        msg = "Nyheter SOFT"
        NewsFeed = feedparser.parse("https://www.svenskorientering.se/lastasidor/IONF?complete=1")
        for i in range (3):
            entry = NewsFeed.entries[i]
            msg = msg + "-" + entry.title + " " + entry.link + "\n"
        await message.channel.send(msg)

    # Shows todays competitions
    if message.content == "!Comp":
        headers = {"ApiKey": EVENTOR_KEY}
        page = requests.get('https://eventor.orientering.se/api/events?fromDate=2020-04-19&toDate=2020-04-19&EventClassificationId', headers=headers)

        with open('EvAn.xml', 'wb') as f:
            f.write(page.content)

        tree = ET.parse('EvAn.xml')
        root = tree.getroot()
        msg = "Tävlingar idag: \n"
        for events in root.findall('Event'):
            rank = events.find('EventId').text
            name = events.find('Name').text
            evId = events.find('EventClassificationId').text
            if evId == "1" or evId == "2" or evId == "3" or evId == "4" or evId == "5":
                msg = msg + "-" + name + " " + rank + " " + evId + "\n"
        await message.channel.send(msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')


client.run(TOKEN)