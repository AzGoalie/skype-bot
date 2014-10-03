# -*- coding: utf-8 -*-

import random
import re

# Used for youtube titles
import json
import urllib2
import urlparse

# Used for imgur title
from BeautifulSoup import BeautifulSoup

# Catfacts
from catfacts import catfacts

# Chatbot
from chatterbotapi import ChatterBotFactory, ChatterBotType

# Trivia
import trivia

# Globals
import config

def doCommand(Message, Status):
    if (Message.FromDisplayName != "Skype Bot" and (Status == 'SENT' or Status == 'RECEIVED')):
        if Message.Body == '!ping':
            ping(Message)
	elif Message.Body == '!help':
	    help(Message)
	elif Message.Body =='!catfact':
	    catfact(Message)
	elif Message.Body.startswith('!roll'):
            roll(Message)
	elif 'youtube.com/watch?v=' in Message.Body:
	    youtube(Message)
	elif 'imgur.com/' in Message.Body and not 'i.im':
	    imgur(Message)
	elif Message.Body == '!botstart' and not config.trivia:
	    botstart(Message)
	elif Message.Body == '!botend':
	    botend(Message)
	elif (Message.Body.startswith('!') and config.chatbotOn and not config.trivia):
	    bot(Message)
	elif Message.Body == '!trivia' and not config.chatbot:
	    trivia.triviaStart(Message)
	elif config.trivia and not config.chatbotOn:
	    if Message.Body.startswith('!'):	#There are hidden commands in the trivia loop...
		trivia.triviaLoop(Message)
        else:
            pass

    else:
        pass

def ping(Message):
    Message.Chat.SendMessage('pong')
    print 'Ping Command Recieved'

def help(Message):
    Message.Chat.SendMessage("Current list of commands:\n!ping - pings the bot to see if its online\n!roll x - rolls a dice of x sides (default 6)\n!catfact - Says an informational fact about cats\n!bot to talk to the bot!\n!trivia to toggle the trivia game!\nWill respond to youtube and imgur links and post the title")

def youtube(Message):
    url_data = urlparse.urlparse(Message.Body)
    query = urlparse.parse_qs(url_data.query)
    video = query['v'][0]
    data = json.loads(urllib2.urlopen(config.API_P1 + video + config.API_P2).read())
    title = data['items'][0]['snippet']['title']
    if title:
        Message.Chat.SendMessage(title + ' - Youtube')
    print 'Youtube Command Recieved'
	
def imgur(Message):
    url = re.search("(?P<url>https?://[^\s]+)", Message.Body).group("url")
    soup = BeautifulSoup(urllib2.urlopen(url))
    try:
    	title = ' '.join(soup.title.string.split())
    	if title:
	    Message.Chat.SendMessage(title)
    	print 'Imgur Command Recieved: ' + title
    except:
	print 'No title Found - Imgur'
def roll(Message):
    sides = [token for token in Message.Body.split() if token.isdigit()]
    if not sides:
        sides = [6]
    roll = random.randint(1,int(sides[0]))
    Message.Chat.SendMessage(Message.FromDisplayName + " rolled a " + str(roll))
    if roll == 420:
	Message.Chat.SendMessage("[̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅][̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅][̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅][̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅][̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅][̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅]")
	Message.Chat.SendMessage('♫♪ |̲̅̅●̲̅̅|̲̅̅=̲̅̅|̲̅̅●̲̅̅| ♫♪ Smoke weed everyday ♫♪ |̲̅̅●̲̅̅|̲̅̅=̲̅̅|̲̅̅●̲̅̅| ♫♪')
	Message.Chat.SendMessage('[̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅][̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅][̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅][̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅][̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅][̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅]')
    print 'Roll Command Recieved'

def catfact(Message):
    Message.Chat.SendMessage(random.choice(catfacts))
    print 'Catfacts Command Recieved'
	
def botstart(Message):
    if not config.chatbotOn:
	config.chatbotOn = True
	config.chatbot = ChatterBotFactory().create(ChatterBotType.CALLMOM, 'f72a7d671e345ab3')
	config.chatbotSession = config.chatbot.create_session()
	Message.Chat.SendMessage('Chatbot Started: Use "!*text*" to talk to it!')
	print 'Chatbot started'
    else:
	print 'bot is already on'
	
def bot(Message):
    if config.chatbotOn:
	s = Message.Body.replace('!bot ', '', 1)
	s = config.chatbotSession.think(s)
	print 's1'
	s = BeautifulSoup(s)
	print 's2'
	s = ''.join(s.findAll(text=True))
	print 's3'	
	Message.Chat.SendMessage(s)
	print 'Bot Command Recieved'
    else:
	print 'bot is off'
		
def botend(Message):
    if config.chatbotOn:
	config.chatbotOn = False
	Message.Chat.SendMessage('Chatbot is now off')
	print 'Chatbot Turned Off'
    else:
	print 'bot is already off'
