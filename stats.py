import os

numLines = 0
numHis = 0
numYs = 0
<<<<<<< HEAD
numRips = 0
=======
>>>>>>> 2c319346392a589ed469481bb3ddcea7683abd5e
statsFile = 'stats.txt'

def setupStats():
	global numLines
	global numHis
	global numYs
	global numRips
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
			if (split[0] == 'y'):
				numYs = int(split[1])
<<<<<<< HEAD
			if (split[0] == 'rip'):
				numRips = int(split[1])
=======
>>>>>>> 2c319346392a589ed469481bb3ddcea7683abd5e
	except:
		f = open(statsFile, 'w+')
		f.close()
	print 'stats initialized'

def stats(msg):
	global numLines
	global numHis
	global numYs
<<<<<<< HEAD
	global numRips

=======
>>>>>>> 2c319346392a589ed469481bb3ddcea7683abd5e
	numLines += 1
	if (msg.Body.lower() == 'hi'):
		numHis += 1
		saveStats()
	if (msg.Body.lower() == 'y'):
		numYs += 1
		saveStats()
<<<<<<< HEAD
	if (msg.Body.lower() == 'rip'):
		numRips += 1
		saveStats()

def printStats(msg):
	s = str(numHis) + ' hi\'s (' + "{0:.2f}%)".format(float(numHis)/numLines * 100) + '\n'
	s += str(numYs) + ' y\'s (' + "{0:.2f}%)".format(float(numYs)/numLines * 100) + '\n'
	s += str(numRips) + ' rip\'s (' + "{0:.2f}%)".format(float(numRips)/numLines * 100) + '\n'
	s += 'Total lines: ' + str(numLines) + '\n'	
=======

def printStats(msg):
	s = str(numHis) + ' hi\'s in ' + str(numLines) + ' messages\n'
	s += str(numYs) + ' y\'s' + '\n'
>>>>>>> 2c319346392a589ed469481bb3ddcea7683abd5e
	msg.Chat.SendMessage(s)
	print s

def saveStats():
	f = open(statsFile, 'w')
	f.write('lines:' + str(numLines) + '\n')
	f.write('hi:' + str(numHis) + '\n')
	f.write('y:' + str(numYs) + '\n')
<<<<<<< HEAD
	f.write('rip:' + str(numRips) + '\n')
=======
>>>>>>> 2c319346392a589ed469481bb3ddcea7683abd5e
	f.close()
