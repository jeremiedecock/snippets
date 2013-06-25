#!/usr/bin/env python

# run:
#   mpirun -np 4 python point_to_point.py
#     or
#   mpiexec -n 4 python point_to_point.py

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank

if rank == 0:
   data = {'key1': [1, 2.5, 3], 'key2': ('hello', 'world')}
else:
   data = None

data = comm.bcast(data, root=0)

print "process", rank, ":", data

