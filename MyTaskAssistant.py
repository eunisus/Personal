#!/usr/bin/python

import sys
import datetime
import time
import re
import logging
from logging.handlers import TimedRotatingFileHandler

# Switch Case implementation
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

def main(argv):
	# Retrieve the arguments
	logLine = sys.argv[1]

	# Configure logging
	logger = logging.getLogger('MyTaskLogger')
	hdlr = TimedRotatingFileHandler('/var/tmp/MyTaskLogger', when='W6')
	formatter = logging.Formatter('%(asctime)-15s [%(levelname)s] %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 
	logger.setLevel(logging.DEBUG)
	
	
	# If the argument contains any form of 'no', just return
	if logLine.lower() in ['no', 'n', 'nope']:
		return

	# If the logLine starts with i or w or e or 
	firstOpt = logLine[:1]
	if firstOpt in ['e', 'l', 'w', 'd']:
		logLine = logLine[1:]

	textToBePrepended = ""

	# Check for the Project Option and extract it
	matchProjectOption = re.search(r'.*(p:[a-zA-Z0-9]+) .*', logLine, re.I)
	if matchProjectOption:
		matchProjectOption = matchProjectOption.group(1)
	if matchProjectOption:
		matchProjectOption = re.search(r'p:(.*)', matchProjectOption, re.I)
	if matchProjectOption:
		matchProjectOption = matchProjectOption.group(1)
	
	if matchProjectOption:
		textToBePrepended = textToBePrepended + '[PROJECT:' \
		+ matchProjectOption \
		+ ']'
	
	# Remove the project option from the log line
	logLine = re.sub('(p:[a-zA-Z0-9]+)', '', logLine)

	# Add a space if textToBePrepended is not empty
	if textToBePrepended and not textToBePrepended.isspace():
		textToBePrepended += " "

	# Check for the Tag Option and extract it
	matchTagOption = re.search(r'.*(t:[a-zA-Z0-9]+) .*', logLine, re.I)
	if matchTagOption:
		matchTagOption = matchTagOption.group(1)
	if matchTagOption:
		matchTagOption = re.search(r't:(.*)', matchTagOption, re.I)
	if matchTagOption:
		matchTagOption = matchTagOption.group(1)

	if matchTagOption:
		textToBePrepended = textToBePrepended + '[TAG:' \
		+ matchTagOption \
		+ ']'

	# Remove the Tag option from the log line
	logLine = re.sub('(t:[a-zA-Z0-9]+)', '', logLine)

	# Create the log that needs to be sent to Logger
	logToBePrinted = textToBePrepended + " " + logLine + " "
	
	# Log with appropriate log level
	for case in switch(firstOpt):
		if case('e'): logger.error(logToBePrinted); break # Log error
		if case('w'): logger.warning(logToBePrinted); break # Log warn
		if case('l'): logger.info("[LEARNING] " + logToBePrinted); break
		if case('d'): logger.debug(logToBePrinted); break # Log debug
		logger.info(logToBePrinted)

	print logToBePrinted

if __name__ == '__main__':
	main(sys.argv[1])
