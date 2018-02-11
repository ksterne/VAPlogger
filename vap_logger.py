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

# Default starting number for QSO count number
count=1

# Setup QSO list/dictionary?
qso = {}
qso['band'] = []
qso['myqth'] = []
qso['mynum'] = []
qso['yourcall'] = []
qso['yournum'] = []
qso['yourqth'] = []

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
    print "Reading in current log at: %s" % opts.log
    # Then lets read in current data
    with open(opts.log, 'r') as readf:
        line = readf.readline()
        while line:
#            print line
#            spline = line.split(' ')
#            print spline
            count=int(line[42:45].strip(' ').lstrip('0'))
#            print count

            line = readf.readline()
        # increment count value by one to show next QSO
        count += 1


# Need to add initial setup
timenow = dt.datetime.utcnow()
print "The current time is: " + str(timenow)

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

        print "Current Frequency band: "+str(band)
        print "f1: change QTH, f2: change band"
        entry = raw_input('Please enter QSO number '+str(count).zfill(3)+': ')

#        print entry
        entry.strip('\n')

        # Give an input to stop the program
        if entry in "exit" or entry in "quit":
            print "Now exiting..."
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
#        print newqso
#        print len(newqso)
        if len(newqso) != 3:
            print "Invalid format, please enter QSO as: callsign,serial#,QTH"
            continue

        yourcall = newqso[0].upper().strip(' ')
        yournum = newqso[1].strip(' ')
        yourqth = newqso[2].strip(' ')


#        if entry in counties["abbrev"] or entry in counties["name"]:
# This may be more useful in the future with some kind of
# auto-complete search
        if yourqth in counties["abbrev"] or yourqth.upper() in counties["abbrev"]:
            # Make sure the QTH value is uppercase
            yourqth = yourqth.upper()
        elif yourqth in counties["name"]:
#            print 'Pull out abbrev'
            some="two"
        elif yourqth in states['abbrev'] or yourqth.upper() in states['abbrev']:
            # Make sure the QTH value is uppercase
            yourqth = yourqth.upper()
        elif yourqth in province['abbrev'] or yourqth.upper() in provnice['abbrev']:
            # Make sure the QTH value is uppercase
            yourqth = yourqth.upper()
        elif yourqth in "DX":
            some="three"
        else:
            print 'QTH {} not valid, please try again'.format(yourqth)
            continue



        # Here we'll need to do dupe checking before going on





        # Lets start to form the output message
        qsostring = "QSO: " + "{:>6}".format(band) + " PH "
        # Lets grab the current time
        nowtime = dt.datetime.utcnow().strftime('%Y-%m-%d %H%M')
        qsostring += str(nowtime) + " " + "{:10}".format(mycall)
        qsostring += " " + str(count).zfill(3) + " " + "{:7}".format(myqth)
        qsostring += "{:10}".format(yourcall) + " " + yournum.zfill(3)
        qsostring += " " + yourqth + "\n"
        print qsostring

        logit = raw_input('Log it? ').strip('\n')
        if logit in "y" or logit in "yes" or logit.upper() in "Y":
            with open(opts.log, 'a') as logfile:
               logfile.write(qsostring)
            # Let's add to the qso dictionary for dupe checking
            qso['band'].append(band)
            qso['myqth'].append(myqth)
            qso['mynum'].append(str(count).zfill(3))
            qso['yourcall'].append(yourcall)
            qso['yournum'].append(yournum.zfill(3))
            qso['yourqth'].append(yourqth)
#            print qso['band']
#            print qso['yourcall']
#            print qso['yournum']
#            print qso['yourqth']

            print "Logged!"
            count += 1
        else:
            print "Not logged"



except KeyboardInterrupt:
    print '\nInterrupted and exiting...'
