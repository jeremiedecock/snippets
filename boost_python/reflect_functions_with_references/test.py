#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cppfunctions

print
print "* cppfunctions.reference_wrong(x):", # CAN'T WORK, NUMBERS ARE IMMUTABLES OBJECTS -> THEY CAN'T BE PASSED BY REFERENCE !
try:
    x = 0.0
    cppfunctions.reference_wrong(x)
    print x
except:
    print sys.exc_info()[0]
    print sys.exc_info()[1]

print "  => ERROR: CAN'T WORK, NUMBERS ARE IMMUTABLES OBJECTS -> THEY CAN'T BE PASSED BY REFERENCE"
print

###################

print "* cppfunctions.reference_right(x):",  # USER DEFINED CLASSES ARE MUTTABLES -> THEY CAN BE PASSED BY REFERENCE !
x = cppfunctions.MuttableNumber()
x.value = 0.0
cppfunctions.reference_right(x)
cppfunctions.reference_right(x)
print x.value

print "  => OK: USER DEFINED CLASSES ARE MUTTABLES -> THEY CAN BE PASSED BY REFERENCE"
print

#help(cppfunctions)
