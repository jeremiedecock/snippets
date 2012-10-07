#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cppclasses

# POINT2D #############################

p1 = cppclasses.Point2D(1.0, 2.0)

print
print "p1:", p1.get_x(), p1.get_y()

p1.set_x(3.0);
p1.set_y(4.0);

print "p1:", p1.get_x(), p1.get_y()
print "p1.to_string():", p1.to_string()

# POINT3D #############################

p2 = cppclasses.Point3D(1.0, 2.0, 3.0)

print
print "p2:", p2.get_x(), p2.get_y(), p2.get_z()

p2.set_x(4.0);
p2.set_y(5.0);
p2.set_z(6.0);

print "p2:", p2.get_x(), p2.get_y(), p2.get_z()
print "p2.to_string():", p2.to_string()
print

#help(cppclasses)
