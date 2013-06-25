#!/usr/bin/env python

# run:
#   mpirun -np 4 python hello.py
#     or
#   mpiexec -n 4 python hello.py

from mpi4py import MPI

rank = MPI.COMM_WORLD.rank
size = MPI.COMM_WORLD.size
name = MPI.Get_processor_name()

print "process %d of %d on %s" % (rank, size, name)

