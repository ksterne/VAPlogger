#! /usr/bin/python
# Logging program for VA QSO party.

# Reads in county, multiplier data from va_list.py


import argparse
import datetime as dt
import os.path
import sys

from va_list import *

#print counties
#print counties["abbrev"]
#print counties["name"]
mycall=None
myqth=None
band=None

count=1

parser = argparse.ArgumentParser(description='VA QSO party options')
parser.add_argument('-c', '--config', type=argparse.FileType('r'), help="Config file to load in defaults")
parser.add_argument('-l', '--log', default='default.txt', help="Log filename to read/save to")


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

# Check to see if logfile name exists
if os.path.isfile(opts.log):
    # Then lets read in current data
    with open(opts.log, 'r') as readf:
        line = readf.readline()
        print line
        while line:
            print line
            line = readf.readline()

# Need to add initial setup
timenow = dt.datetime.utcnow()
print timenow

# Ask for call sign if not set with config file
if mycall is None:
    mycall = raw_input('Please enter your callsign: ')
# Ask for location if not set with config file
if myqth is None:
    myqth = raw_input('Please enter your location: ')
if band is None:
    band = raw_input('Please enter frequency band in kHz: ')


try:
    while (1):

        print "Frequency band: "+str(band)
        print "f1: change QTH, f2: change band"
        entry = raw_input('Please enter QSO number '+str(count).zfill(3)+': ')

#        print entry
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
        elif entry.lower() in "f2":
            band = raw_input('Please enter new band in kHz: ').strip('\n')
            continue


        # Assume format of callsign,number,qth
        newqso = entry.split(',')
        print newqso
# Come back to this later
#        print len(newqso)
#        if len(newqso) < 3:
#            print "Invalid format, please enter QSO as: callsign, serial#, QTH"
#            continue

        yourqth = newqso[2].strip(' ')


#        if entry in counties["abbrev"] or entry in counties["name"]:
# This may be more useful in the future with some kind of
# auto-complete search
        if yourqth in counties["abbrev"] or yourqth.upper() in counties["abbrev"]:
#            print 'hi!'
            some="one"
        elif yourqth in counties["name"]:
#            print 'Pull out abbrev'
            some="two"
        elif yourqth in "DX":
            some="three"
        else:
            print 'QTH {} not valid, please try again'.format(yourqth)
            continue

        # Lets start to form the output message
        qsostring = "QSO: " + band + " PH "
        # Lets grab the current time
        nowtime = dt.datetime.utcnow().strftime('%Y-%m-%d %H%M')
        qsostring += str(nowtime) + " " + "{:10}".format(mycall)
        qsostring += " " + str(count).zfill(3) + " " + "{:7}".format(myqth)
        qsostring += "{:10}".format(newqso[0]) + " " + newqso[1]
        qsostring += " " + yourqth + "\n"
        print qsostring

        logit = raw_input('Log it? ').strip('\n')
        if logit in "y" or logit in "yes" or logit.upper() in "Y":
            with open(opts.log, 'a') as logfile:
               logfile.write(qsostring)
            print "Logged!"
            count += 1
        else:
            print "Not logged"



except KeyboardInterrupt:
    print '\nInterrupted and exiting...'
