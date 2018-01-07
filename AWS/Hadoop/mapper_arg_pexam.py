#!/usr/bin/env python
import sys
import re

regDigit = re.compile("^\d+\\.{0,1}\d*$")
arg1 = str(sys.argv[1])
arg2 = str(sys.argv[2])
arg3 = str(sys.argv[2])

# arg1 = str(173)
# arg2 = str(183)
# with open ('data3.csv') as csvfile:
for line in sys.stdin:
#     for line in csvfile:
    line = line.strip()
    line = line.split(",")
    #print(line)

    if len(line)>0:
        # print line[2]
        if (regDigit.match(line[1])) and line[1] == arg3 and line[2] > arg1 and line[2] < arg2:
        #x = 1 if (regDigit.match(line[11]) and float(line[11]) > 0) else 0
        # if (regDigit.match(line[11]) and float(line[11])>0):
        #     line[11]=1
        # else:
        #     line[11]=0
            print '%s,%s,%s' % (line[1],line[2],1)


