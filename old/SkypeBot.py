#!/usr/bin/env python
import Skype4Py

# Dice
import random

# Used for youtube titles
import json
import urllib2
import urlparse

# Catfacts
from catfacts import catfacts
import sched
import time

# Cleverbot
from chatterbotapi import ChatterBotFactory, ChatterBotType
cleverbot = None
cleverbotSession = None

API_P1 = 'https://www.googleapis.com/youtube/v3/videos?id='
API_P2 = '&key=AIzaSyBvL5DKHluKpCM2B6S32gPOL4lNIW3Y6xc&fields=items(snippet(title))&part=snippet'

def commands(Message, Status):
    if Status == 'SENT' or (Status == 'RECEIVED'):
        if Message.Body == "!ping":
            cmd_ping(Message)
        elif "!roll" in Message.Body:
            cmd_roll(Message)
	elif "youtube.com/watch?v=" in Message.Body:
	    cmd_youtube(Message)
	elif Message.Body == "!help":
	    cmd_help(Message)
	elif Message.Body == "!catfact":
	    cmd_catfacts(Message)
	elif Message.Body == "!autocatfacts":
	    cmd_autocatfacts()
	elif Message.Body == "!botstart":
	    cmd_botstart(Message)
	elif "!bot" in Message.Body:
	    pass
        else:
            pass

    else:
        pass

def cmd_ping(Message):
    Message.Chat.SendMessage('pong')
    print "Ping Command Received \n"

def cmd_roll(Message):
    if Message.Sender.FullName == skype.CurrentUser.FullName:
        return
    sides = [token for token in Message.Body.split() if token.isdigit()]
    if not sides:
        sides = [6]
    roll = random.randint(1,int(sides[0])+1)
    Message.Chat.SendMessage(Message.Sender.FullName + " rolled a " + str(roll))
    print "Roll Command Recieved \n"

def cmd_youtube(Message):
    url_data = urlparse.urlparse(Message.Body)
    query = urlparse.parse_qs(url_data.query)
    video = query["v"][0]
    data = json.loads(urllib2.urlopen(API_P1 + video + API_P2).read())
    title = data['items'][0]['snippet']['title']
    if title:
        Message.Chat.SendMessage('Video Title: ' + title)
    print 'Youtube Command Recieved\n'

def cmd_catfacts(Message):
    Message.Chat.SendMessage(random.choice(catfacts))
    print 'Catfacts Command Recieved\n'

def cmd_help(Message):
    Message.Chat.SendMessage("Current list of commands:\n!ping - pings the bot to see if its online\n!roll x - rolls a dice of x sides (default 6)\n!catfact - Says an informational fact about cats\nWill respond to youtube links and post the title")

def cmd_botstart(Message):
    global cleverbot
    global cleverbotSession
    cleverbot = ChatterBotFactory().create(ChatterBotType.CLEVERBOT)
    cleverbotSession = cleverbot.create_session()
    Message.Chat.SendMessage("Cleverbot Started: Use ( ! )bot to talk to it!")
    print "Cleverbot started\n"

def cmd_cleverbot(Message):
    s = Message.Body.replace('!bot ', '', 1)
    s = cleverbotSession.think(s)
    Message.Chat.SendMessage(s)
    print 'Bot Command Recieved\n'

skype = Skype4Py.Skype();
skype.OnMessageStatus = commands

if skype.Client.IsRunning == False:
    skype.Client.Start()
skype.Attach();

print 'Skype Bot currently running on user',skype.CurrentUserHandle, "\n"

while True:
    raw_input('')
