#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cppclasses

pt = cppclasses.Point()
pt.x = 0.0
pt.y = 0.0

foo = cppclasses.Foo(pt)
foo.translate()
foo.translate()

print "(", pt.x, ",", pt.y, ")"

#help(cppclasses)
