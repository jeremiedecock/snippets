#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cppclasses

# Hello #############################

print
print '*** Instanciate "Hello" ***'
print

msg = cppclasses.Hello("Joe")

# HelloFr ###########################

print
print '*** Extend "Hello" from Python ***'
print

# INITIALIZATION LIST IS IMPLICITLY BRING TO HELLO !
class HelloFr(cppclasses.Hello):
    def __init__(self, _name):
        print "Bonjour", _name, "!"

msg = HelloFr("John")

print

#help(cppclasses)
