#! /usr/bin/python
# Logging program for VA QSO party.

# Reads in county, multiplier data from va_list.py


import datetime as dt

from va_list import *


#print counties
print counties["abbrev"]
print counties["name"]

# Need to add initial setup
timenow = dt.datetime.utcnow()
print timenow
# Ask for call sign
mycall = raw_input('Please enter your callsign: ')
# Ask for location
myqth = raw_input('Please entery your location: ')


try:
    while (1):

        entry = raw_input('Please enter new QSO: ')

        print entry
        entry.strip('\n')

        if entry in counties["abbrev"] or entry in counties["name"]:
            print 'hi!'
        else:
            print ':('

except KeyboardInterrupt:
    print '\nInterrupted and exiting...'
