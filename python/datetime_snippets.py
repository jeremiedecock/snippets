#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

# Datetime ############################

dt = datetime.datetime.now()
print(dt)

dt = datetime.datetime(year=2018, month=8, day=30, hour=13, minute=30)
print(dt)

print(dt.isoformat())

# Date ################################

d = datetime.date.today()
print(d)

d = datetime.datetime.now().date()
print(d)

d = datetime.date(year=2018, month=8, day=30)
print(d)

print(d.isoformat())

# Time ################################

t = datetime.datetime.now().time()
print(t)

t = datetime.time(hour=1, minute=30)
print(t)

print(t.isoformat())
