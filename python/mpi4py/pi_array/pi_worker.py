#!/usr/bin/env python3

from mpi4py import MPI
import numpy as np
import math

comm = MPI.Comm.Get_parent()
num_proc = comm.Get_size()
rank = comm.Get_rank()

data = np.array(0, dtype='i')
comm.Bcast([data, MPI.INT], root=0)

print("[worker {0}] data = {1}".format(rank, data))

h = 1.0 / float(data)
s = 0.0

# \pi/4 = \integ_0^1{\sqrt(1-x^2) dx}
for i in range(rank, data, num_proc):
    x = h * (i + 0.5)
    s += math.sqrt(1.0 - x**2) * h

result = np.array(4.0 * s, dtype='d')
comm.Reduce([result, MPI.DOUBLE], None, op=MPI.SUM, root=0)

comm.Disconnect()
