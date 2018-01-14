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

count=1

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

        entry = raw_input('Please enter QSO number '+str(count).zfill(3)+' (f1 change QTH): ')

        print entry
        entry.strip('\n')

        # Give an input to stop the program
        if entry in "exit" or entry in "quit":
            sys.exit()

        if entry.lower() in "f1":
            myqth = raw_input('Enter new QTH: ').strip('\n')
            while myqth not in counties["abbrev"]:
                print myqth + " not found in counties list"
                myqth = raw_input('Please enter new QTH: ').strip('\n')

            continue


#        if entry in counties["abbrev"] or entry in counties["name"]:
        if entry in counties["abbrev"]:
            print 'hi!'
        elif entry in counties["name"]:
            print 'Pull out abbrev'
        else:
            print ':('

        logit = raw_input('Log it? ').strip('\n')
        if logit in "y" or logit in "yes" or logit.upper() in "Y":
            print "Logged!"
            count += 1
        else:
            print "Not logged"



except KeyboardInterrupt:
    print '\nInterrupted and exiting...'
