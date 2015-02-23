import datetime
import os

numLines = 0
numHis = 0
statsFile = 'stats.txt'
startDate = ''

def setupStats():
	global numLines
	global numHis
	global startDate
	try:
		f = open(statsFile, 'r')
		for line in f:
			split = line.split(':')
			if (split[0] == 'lines'):
				numLines = int(split[1])
			if (split[0] == 'start'):
				startDate = split[1] + split[2] + split[3] + split[4] #date + h:m:s
			if (split[0] == 'hi'):
				numHis = int(split[1])
		if (startDate == ''):
			startDate = datetime.datetime.now()
	except:
		f = open(statsFile, 'w+')
		f.close()
	print 'stats initialized'

def stats(msg):
	global numLines
	global numHis
	numLines += 1
	if (msg.Body.lower() == 'hi'):
		numHis += 1
		saveStats()

def printStats(msg):
	s = str(numHis) + ' hi\'s in ' + str(numLines) + ' messages since ' + str(startDate)
	msg.Chat.SendMessage(s)
	print s

def saveStats():
	f = open(statsFile, 'w')
	f.write('lines:' + str(numLines) + '\n')
	f.write('hi:' + str(numHis) + '\n')
	f.write('start:' + str(startDate) + '\n')
	f.close()
