#!/usr/bin/env python

from mpi4py import MPI

comm = MPI.Comm.Get_parent()

size = comm.size
rank = comm.rank

data = None
data = comm.bcast(data, root=0)

print "process", rank, ":", data

comm.Disconnect()
