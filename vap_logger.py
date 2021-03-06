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
qso['time'] = []
qso['myqth'] = []
qso['mynum'] = []
qso['yourcall'] = []
qso['yournum'] = []
qso['yourqth'] = []

mults = []

score = 0
qsopoints = 0

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
            qso['band'].append(line[5:11].strip(' '))
            qso['time'].append(line[15:30])
            qso['mynum'].append(line[42:45])
            qso['myqth'].append(line[46:49])
            qso['yourcall'].append(line[53:63].strip(' '))
            qso['yournum'].append(line[64:67])
            qso['yourqth'].append(line[68:71].strip('\n'))
            count=int(line[42:45].strip(' ').lstrip('0'))

            # Load in current multipliers
            linemult = line[68:71].strip('\n')
            if linemult not in mults:
#                print "New mult found!"
#                print linemult
#                print mults
                mults.append(linemult)

#            print qso['myqth'].count(line[46:49])
            if (qso['myqth'].count(line[46:49]) > 9
                and line[46:49] not in mults):
#                print "New mult from 10 or more QSOs!"
                mults.append(line[46:49])

            # Lets start figuring an initial score value
            # Total up number of qso points, VA mobiles are 3!
            if '/M' in line[53:63].strip(' ') and line[68:71] in counties['abbrev'] :
                qsopoints += 3
            else:
                qsopoints += 1


            line = readf.readline()
        # increment count value by one to show next QSO
        count += 1

#print len(mults)
#print mults
#print len(set(qso['myqth']))
#print qsopoints
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

# Crude way to do a "band" for now. Most ham bands will
# fit into the +/- 300 kHz range
bandrange = [ int(band)-300, int(band)+300]

#print bandrange


try:
    while (1):

        print ""
        print "Last few QSOs:"
        # For now just leave this as the last five
        if count > 5:
            print '%s  %s %-9s %-9s  %s  %s ' % (qso['time'][count-6],
                qso['mynum'][count-6], qso['myqth'][count-6],
                qso['yourcall'][count-6], qso['yournum'][count-6],
                qso['yourqth'][count-6])
        if count > 4:
            print '%s  %s %-9s %-9s  %s  %s ' % (qso['time'][count-5],
                qso['mynum'][count-5], qso['myqth'][count-5],
                qso['yourcall'][count-5], qso['yournum'][count-5],
                qso['yourqth'][count-5])
        if count > 3:
            print '%s  %s %-9s %-9s  %s  %s ' % (qso['time'][count-4],
                qso['mynum'][count-4], qso['myqth'][count-4],
                qso['yourcall'][count-4], qso['yournum'][count-4],
                qso['yourqth'][count-4])
        if count > 2:
            print '%s  %s %-9s %-9s  %s  %s ' % (qso['time'][count-3],
                qso['mynum'][count-3], qso['myqth'][count-3],
                qso['yourcall'][count-3], qso['yournum'][count-3],
                qso['yourqth'][count-3])
        if count > 1:
            print '%s  %s %-9s %-9s  %s  %s ' % (qso['time'][count-2],
                qso['mynum'][count-2], qso['myqth'][count-2],
                qso['yourcall'][count-2], qso['yournum'][count-2],
                qso['yourqth'][count-2])

        # Score is qso pitns multiplied by number of mults plus Bonus points.
        # Bonus points for mobile, 100 points per each myqth
        score = (qsopoints*len(mults))+(len(set(qso['myqth']))*100)
        print "Current Frequency band: "+str(band)+ "  Current score:"+str(score)
        print "f1: change QTH, f2: change band"
        print ""
        entry = raw_input('Please enter QSO number '+str(count).zfill(3)+': ')

#        print entry
        entry.strip('\n')
        duped = False

        # Give an input to stop the program
        if entry in "exit" or entry in "quit":
            print "Now exiting..."
            sys.exit()

        if entry.lower() in "f1":
            myqth = raw_input('Enter new QTH: ').strip('\n')
            myqth = myqth.upper()
            while myqth not in counties["abbrev"]:
                print myqth + " not found in counties list"
                myqth = raw_input('Please enter new QTH: ').strip('\n')

            continue
        elif entry.lower() in "f2":
            band = raw_input('Please enter new band in kHz: ').strip('\n')
            # Update the band range
            bandrange = [ int(band)-300, int(band)+300]
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
        elif yourqth in province['abbrev'] or yourqth.upper() in province['abbrev']:
            # Make sure the QTH value is uppercase
            yourqth = yourqth.upper()
        elif yourqth in "DX":
            some="three"
        else:
            print 'QTH {} not valid, please try again'.format(yourqth)
            continue


        # Here we'll need to do dupe checking before going on
        if yourcall in qso['yourcall']:
#            print "Found duplicate call at least"
            # Find all of the places where the callsign matches
            callindexes = [ i for i,x in enumerate(qso['yourcall']) if x == yourcall]
#            print callindexes
            for x in callindexes:
                if bandrange[0] < int(qso['band'][x]) < bandrange[1]:
                    if qso['myqth'][x] in myqth:
                        if qso['yourqth'][x] in yourqth:
                            print ""
                            print "********"
                            print "Duplicate entry: %s  %s  %s    %s  %s  %s" % (mycall,
                                   qso['mynum'][x], qso['myqth'][x], qso['yourcall'][x],
                                   qso['yournum'][x], qso['yourqth'][x])
                            print "*******"
                            print ""
                            # Mark duplicate flag as true!
                            duped = True

        # If duplicate found, don't give the option to log it
        if duped:
            duped = False
            continue


        qso['time'].append(dt.datetime.utcnow().strftime('%Y-%m-%d %H%M'))

        # Lets start to form the output message
        qsostring = "QSO: " + "{:>6}".format(band) + " PH "
        # Lets grab the current time
        nowtime = dt.datetime.utcnow().strftime('%Y-%m-%d %H%M')
        qsostring += str(nowtime) + " " + "{:10}".format(mycall)
        qsostring += " " + str(count).zfill(3) + " " + "{:7}".format(myqth)
        qsostring += "{:10}".format(yourcall) + " " + yournum.zfill(3)
        qsostring += " " + yourqth + "\r\n"
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

            if (qso['myqth'].count(myqth) > 9
                and myqth not in mults):
                print "New multiplier from 10 or more QSOs here!!!"
                mults.append(myqth)

            # Check for new multiplier
            if yourqth not in mults:
                print "New multiplier!!!"
                mults.append(yourqth)

            # Update the QSO points for real-time scoring
            if '/M' in yourcall and yourqth in counties['abbrev']:
                qsopoints += 3
            else:
                qsopoints += 1

            print "Logged!"
            count += 1
        else:
            print "Not logged"



except KeyboardInterrupt:
    print '\nInterrupted and exiting...'
