#!/usr/bin/env python
# coding: utf-8

import datetime


# UTC #################################

# Naive
print(datetime.datetime.utcnow())

# Aware
print(datetime.datetime.now().astimezone(datetime.timezone.utc))

# Local ###############################

# Naive
print(datetime.datetime.now())

# Aware
print(datetime.datetime.now().astimezone(tz=None))

# Local timezone
print(datetime.datetime.now().astimezone(tz=None).tzinfo)
