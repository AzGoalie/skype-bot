import os
import rpg 

numLines = 0
numHis = 0
numYs = 0
numRips = 0
statsFile = 'stats.txt'
 
def setupStats():
	global numLines
	global numHis
	global numYs
	global numRips
	global startDate
 
	rpg.setupRPG()

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
			if (split[0] == 'y'):
				numYs = int(split[1])
			if (split[0] == 'rip'):
				numRips = int(split[1])
	except:
		f = open(statsFile, 'w+')
		f.close()
	print 'stats initialized'
 
def stats(msg):
	global numLines
	global numHis
	global numYs
	global numRips
 
	numLines += 1
	if (msg.Body.lower() == 'hi'):
		numHis += 1
		saveStats()
	if (msg.Body.lower() == 'y'):
		numYs += 1
		saveStats()
	if (msg.Body.lower() == 'rip'):
		numRips += 1
		saveStats()
 
def printStats(msg):
	s = str(numHis) + ' hi\'s (' + "{0:.2f}%)".format(float(numHis)/numLines * 100) + '\n'
	s += str(numYs) + ' y\'s (' + "{0:.2f}%)".format(float(numYs)/numLines * 100) + '\n'
	s += str(numRips) + ' rip\'s (' + "{0:.2f}%)".format(float(numRips)/numLines * 100) + '\n'
	s += 'Total lines: ' + str(numLines) + '\n'
	s += '----------------------------------------\n'
	rpg.currentXP = 83
	rpg.calcLevel()
	s += 'Level: ' + str(rpg.currentLevel) + ' XP: ' + str(rpg.currentXP) + '\n'
	msg.Chat.SendMessage(s)
	print s
 
def saveStats():
	f = open(statsFile, 'w')
	f.write('lines:' + str(numLines) + '\n')
	f.write('hi:' + str(numHis) + '\n')
	f.write('y:' + str(numYs) + '\n')
	f.write('rip:' + str(numRips) + '\n')
	f.close()
	print 'stats saved\n'
