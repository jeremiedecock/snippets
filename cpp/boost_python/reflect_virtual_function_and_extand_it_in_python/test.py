#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cppclasses
import sys

# Hello #############################

print
print '*** Instanciate "Hello" ***'
print

msg = cppclasses.Hello()
msg.message()

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
