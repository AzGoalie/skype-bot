import os
import math

currentXP = 0
currentLevel = 0
rpgFile = 'rpg.txt'

def setupRPG():
	global currentXP
	global currentLevel

	try:
		f = open(rpgFile, 'r')
		for line in f:
			split = line.split(':')
			if (split[0] == 'xp'):
				currentXP = int(split[1])
			if (split[0] == 'level'):
				currentLevel = split[1]
	except:
		f = open(rpgFile, 'w+')
		f.close()
	print 'rpg initialized'

def calcLevel():
	global currentLevel	
	xp = 0
	level = 1

	while currentXP > (xp/4):
		xp += int(level + 300 * math.pow(2, float(level)/7))
		level += 1

	currentLevel = level

def saveRPG():
	f = open(rpgFile, 'w')
	f.write('xp:' + str(currentXP) + '\n')
	f.write('level:' + str(currentLevel) + '\n')
	f.close()
