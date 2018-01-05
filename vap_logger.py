# Logging program for VA QSO party.

# Reads in county, multiplier data from va_list.py


from va_list import *


print counties["abbrev"]
print counties["name"]

try:
    while (1):

        entry = raw_input('Enter new QSO here: ')

#        print entry
        entry.strip('\n')

        if entry in counties["abbrev"] or entry in counties["name"]:
            print 'hi!'
        else:
            print ':('

except KeyboardInterrupt:
    print '\nInterrupted and exiting...'
