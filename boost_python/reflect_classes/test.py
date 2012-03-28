#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cppclasses

p1 = cppclasses.Point(1.0, 2.0)
p2 = cppclasses.Point()

print "p1:", p1.get_x(), p1.get_y()
print "p2:", p2.get_x(), p2.get_y()

#help(cppclasses)
