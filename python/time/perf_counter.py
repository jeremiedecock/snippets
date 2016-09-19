#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

# See: https://docs.python.org/3/library/time.html#time.process_time
#      http://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python

import time

initial_time = time.perf_counter()

#do some stuff
time.sleep(1)

final_time = time.perf_counter()

elapsed_time = final_time - initial_time

print(elapsed_time, "sec")
