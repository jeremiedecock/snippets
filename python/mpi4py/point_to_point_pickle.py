#!/usr/bin/env python

# run:
#   mpirun -np 4 python point_to_point_pickle.py
#     or
#   mpiexec -n 4 python point_to_point_pickle.py

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank

if rank == 0:
    data = {'a': 7, 'b': 3.14}
    comm.send(data, dest=1, tag=11)
elif rank == 1:
    data = comm.recv(source=0, tag=11)
    print data

