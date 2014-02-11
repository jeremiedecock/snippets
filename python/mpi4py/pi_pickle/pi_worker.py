#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

from mpi4py import MPI
import math

comm = MPI.Comm.Get_parent()

num_proc = comm.size
rank = comm.rank

data = None
data = comm.bcast(data, root=0)

print "[worker {0}] data = {1}".format(rank, data)

h = 1.0 / float(data)
s = 0.0

# \pi/4 = \integ_0^1{\sqrt(1-x^2) dx}
for i in range(rank, data, num_proc):
    x = h * (i + 0.5)
    s += math.sqrt(1.0 - x**2) * h

local_result = 4.0 * s

result = comm.reduce(local_result, op=MPI.SUM, root=0)

comm.Disconnect()
