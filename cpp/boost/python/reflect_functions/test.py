#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cppfunctions

print "* cppfunctions.print_on_cout(): ",
cppfunctions.print_on_cout()
print

print "* cppfunctions.one_argument(3.0):",
print cppfunctions.one_argument(3.0)

print "* cppfunctions.two_arguments(2, 3.0):",
print cppfunctions.two_arguments(2, 3.0)

print "* cppfunctions.overload_arguments(3.14):",
print cppfunctions.overload_arguments(3.14)
print "* cppfunctions.overload_arguments(3.14, 3):",
print cppfunctions.overload_arguments(3.14, 3)
print "* cppfunctions.overload_arguments(): ",
print cppfunctions.overload_arguments()
print "* cppfunctions.overload_arguments('hello'): ",
print cppfunctions.overload_arguments('hello')

print "* cppfunctions.default_arguments(1, 2, 3):",
print cppfunctions.default_arguments(1, 2, 3)
print "* cppfunctions.default_arguments(1, 2):",
print cppfunctions.default_arguments(1, 2)
print "* cppfunctions.default_arguments(1):",
print cppfunctions.default_arguments(1)
#print cppfunctions.default_arguments(1, y=2, z=3)
#print cppfunctions.default_arguments(1, y=2)
#print cppfunctions.default_arguments(1, z=3)

print "* cppfunctions.std_string('hello'):",
print cppfunctions.std_string('hello')

print "* cppfunctions.c_string('abc'):",
print cppfunctions.c_string('abc')

print "* cppfunctions.throw_exception(2):",
print cppfunctions.throw_exception(2)
print "* cppfunctions.throw_exception(4):",
try:
    print cppfunctions.throw_exception(4)
except Exception as inst:
    print type(inst),     # the exception instance
    print inst.args,      # arguments stored in .args
    print inst            # __str__ allows args to printed directly

#help(cppfunctions)
