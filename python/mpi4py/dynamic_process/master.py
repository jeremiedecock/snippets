#!/usr/bin/env python

# run:
#   mpirun python master.py
#     or
#   mpiexec python master.py

from mpi4py import MPI
import sys

comm = MPI.COMM_SELF.Spawn(sys.executable, args=['worker.py'], maxprocs=5)

data = (1000, 2000, 3000)
data = comm.bcast(data, root=MPI.ROOT)

print "master:", data

comm.Disconnect()
