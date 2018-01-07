#!/usr/bin/env python

from operator import itemgetter
import sys

current_zip = None
current_ht = None
current_count = 0
a_year = None
a_month = None
scount = None

# with open ('out.txt') as out:
#     for line in out:

for line in sys.stdin:

    line = line.strip()
    #print(line)
    #qdate, mag = line.split(',',1)
    a_year,a_month, scount = line.split(',')
    try:
        scount = int(scount)
    except ValueError:
        continue

    if current_zip == a_year and current_ht==a_month :
        current_count +=scount
    else:
        if current_zip and current_ht :
            print '%s,%s,%s' % (current_zip, current_ht,  current_count)
        current_ht = a_month
        current_zip = a_year
        current_count = scount

if current_zip and current_ht :
    print '%s,%s,%s' % (current_zip, current_ht, current_count)


