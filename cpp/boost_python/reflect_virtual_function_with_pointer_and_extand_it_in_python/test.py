#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cppclasses
import sys

# Geometry ##########################

print
print '*** Instanciate "Geometry" ***'
print

point = cppclasses.Point(1, 2)
print "cpp before: (", point.get_x(), ",", point.get_y(), ")"

geo = cppclasses.Geometry()
geo.translate(point)
print "cpp after: (", point.get_x(), ",", point.get_y(), ")"

# GeometryPy ########################

print
print '*** Extend "Geometry" from Python ***'
print

class GeometryPy(cppclasses.Geometry):
    def translate(self, point):
        point.set_x( point.get_x() + (-1.0 * self.get_translate_value()) )
        point.set_y( point.get_y() + (-1.0 * self.get_translate_value()) )

point = cppclasses.Point(1, 2)
print "cpp before: (", point.get_x(), ",", point.get_y(), ")"

geo = GeometryPy()
geo.translate(point)
print "cpp after: (", point.get_x(), ",", point.get_y(), ")"
print

#help(cppclasses)
