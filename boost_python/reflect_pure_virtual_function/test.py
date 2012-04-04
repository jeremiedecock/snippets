#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cppclasses
import sys

# Hello #############################

print
print '*** Try to instanciate "Hello" (forbidden) ***'
print

try:
    msg = cppclasses.Hello()
    msg.message()
except:
    print sys.exc_info()[0]
    print sys.exc_info()[1]

# HelloFr ###########################

print
print '*** Extend "Hello" from Python ***'
print

class HelloFr(cppclasses.Hello):
    def message(self):
        print "Bonjour", self.get_name(), "!"

msg = HelloFr()
msg.message()

print

#help(cppclasses)
