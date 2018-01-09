#! /usr/bin/python
# Logging program for VA QSO party.

# Reads in county, multiplier data from va_list.py


import argparse
import datetime as dt
import sys

from va_list import *

#print counties
#print counties["abbrev"]
#print counties["name"]
mycall=None
myqth=None


parser = argparse.ArgumentParser(description='VA QSO party options')
parser.add_argument('-c', '--config', type=argparse.FileType('r'), help="Config file to load in defaults")

opts=parser.parse_args()

# Pull initial call and qth out of config file, if set
if opts.config is not None:
    line = opts.config.readline()
    while line:
        if "mycall" in line:
            linelist=line.split()
            mycall = linelist[1]
        elif "myqth" in line:
            linelist=line.split()
            myqth = linelist[1]

        line = opts.config.readline()

# Need to add initial setup
timenow = dt.datetime.utcnow()
print timenow

# Ask for call sign if not set with config file
if mycall is None:
    mycall = raw_input('Please enter your callsign: ')
# Ask for location if not set with config file
if myqth is None:
    myqth = raw_input('Please entery your location: ')


try:
    while (1):

        entry = raw_input('Please enter new QSO: ')

        print entry
        entry.strip('\n')

        # Give an input to stop the program
        if entry in "exit" or entry in "quit":
            sys.exit()



#        if entry in counties["abbrev"] or entry in counties["name"]:
        if entry in counties["abbrev"]:
            print 'hi!'
        elif entry in counties["name"]:
            print 'Pull out abbrev'
        else:
            print ':('



except KeyboardInterrupt:
    print '\nInterrupted and exiting...'
