#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cppfunctions

print
print "* cppfunctions.pointer_wrong(x):", # CAN'T WORK, NUMBERS ARE IMMUTABLES OBJECTS -> THEY CAN'T BE PASSED BY POINTER !
try:
    x = 0.0
    cppfunctions.pointer_wrong(x)
    print x
except:
    print sys.exc_info()[0]
    print sys.exc_info()[1]

print "  => CAN'T WORK, NUMBERS ARE IMMUTABLES OBJECTS -> THEY CAN'T BE PASSED BY POINTER"
print

###################

print "* cppfunctions.pointer_right(x):",  # USER DEFINED CLASSES ARE MUTTABLES -> THEY CAN BE PASSED BY POINTER !
x = cppfunctions.MuttableNumber()
x.value = 0.0
cppfunctions.pointer_right(x)
print x.value

print "  => USER DEFINED CLASSES ARE MUTTABLES -> THEY CAN BE PASSED BY POINTER"
print

#help(cppfunctions)
