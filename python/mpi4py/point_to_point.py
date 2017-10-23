#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# run:
#   mpirun -np 4 python3 point_to_point.py
#     or
#   mpiexec -n 4 python3 point_to_point.py

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank

if rank == 0:
    valeur = 1000
    comm.send(valeur, dest=1)
elif rank == 1:
    valeur = comm.recv(source=0)
    print("proc1: received", valeur, "of proc0.")

