#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cppfunctions

print "* cppfunctions.foo(x):",  # USER DEFINED CLASSES ARE MUTTABLES -> THEY CAN BE PASSED BY POINTER !
x = cppfunctions.MuttableDouble(0.0)
cppfunctions.foo(x)
print x.value
print

print "* cppfunctions.foo(y):",  # USER DEFINED CLASSES ARE MUTTABLES -> THEY CAN BE PASSED BY POINTER !
y = cppfunctions.MuttableDouble()
y.value = 0.0
cppfunctions.foo(y)
print y.value

print
print "  => OK: USER DEFINED CLASSES ARE MUTTABLES -> THEY CAN BE PASSED BY POINTER"
print

#help(cppfunctions)
