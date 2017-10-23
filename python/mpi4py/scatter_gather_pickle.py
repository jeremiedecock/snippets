#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)

# run:
#   mpirun -np 4 python3 scatter_gather_pickle.py | sort
#     or
#   mpiexec -n 4 python3 scatter_gather_pickle.py | sort

from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    data = ['x' + str(i) for i in range(size)]
else:
    data = None

# SCATTER

print("[1. before scatter] process", rank, ":", data)

data = comm.scatter(data, root=0)

print("[2. after scatter] process", rank, ":", data)

# PROCESS DATA

data = data.replace('x', 'y')

# GATHER

print("[3. before gather] process", rank, ":", data)

data = comm.gather(data, root=0)

print("[4. after gather] process", rank, ":", data)

