#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cppclasses

point = cppclasses.Point()

print "(", point.x, ",", point.y, ")"

point.x = 1;
point.y = 1;

print "(", point.x, ",", point.y, ")"

#help(cppclasses)
