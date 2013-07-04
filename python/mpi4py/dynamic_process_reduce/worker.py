#!/usr/bin/env python

from mpi4py import MPI

comm = MPI.Comm.Get_parent()

size = comm.size
rank = comm.rank

data = rank

result = comm.reduce(data, op=MPI.SUM, root=0)

print "process", rank, ":", result

comm.Disconnect()
