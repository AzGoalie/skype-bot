#!/usr/bin/env python
import Skype4Py
import sys

# Globals and settings
from config import skype

from commands import doCommand
from stats import setupStats

if __name__ == '__main__':
	print 'initializing stats'
	setupStats()
	try:
		skype = Skype4Py.Skype();
		print 'Skype4Py Initalized'
	except:
		print 'Failed to load Skype4Py, exiting...'
		sys.exit()

	if skype.Client.IsRunning == True:
		print 'Skype is running'
	else:
		print 'Skype not found, starting...'
	
	try:
		skype.Client.Start()
		print 'Skype Started'
	except:
		print 'Failed to start Skype, exiting...'
		sys.exit()
	try:
		skype.Attach()
		skype.OnMessageStatus = doCommand
	except:
		print 'Skype4Py failed to attach, exiting...'
		sys.exit()
		
	print 'Started Successfully'
	while True:
		raw_input('')
