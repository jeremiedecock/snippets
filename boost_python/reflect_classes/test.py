#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cppclasses

p1 = cppclasses.Point(1.0, 2.0)
p2 = cppclasses.Point()

print "p1:", p1.get_x(), p1.get_y()
print "p2:", p2.get_x(), p2.get_y()

p2.set_x(3);
p2.set_y(4);

print "p1:", p1.get_x(), p1.get_y()
print "p2:", p2.get_x(), p2.get_y()

p1.color = "red"
print "p1 color:", p1.color

print "p1.to_string():", p1.to_string()

#print "number or point:", Point.cpt # TODO: static data member unreachable

#help(cppclasses)
