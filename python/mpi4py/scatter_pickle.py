#!/usr/bin/env python

# run:
#   mpirun -np 4 python scatter_pickle.py | sort
#     or
#   mpiexec -n 4 python scatter_pickle.py | sort

from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    data = [100*i for i in range(size)]
else:
    data = None

print "[before scatter] process", rank, ":", data

data = comm.scatter(data, root=0)

print "[after scatter] process", rank, ":", data
