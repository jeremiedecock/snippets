#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# run:
#   mpirun -np 4 python gather_pickle.py | sort
#     or
#   mpiexec -n 4 python gather_pickle.py | sort

from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

data = rank * 100

print "[before gather] process", rank, ":", data

data = comm.gather(data, root=0)

print "[after gather] process", rank, ":", data

