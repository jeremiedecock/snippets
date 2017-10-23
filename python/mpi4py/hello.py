#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# run:
#   mpirun -np 4 python3 hello.py
#     or
#   mpiexec -n 4 python3 hello.py

from mpi4py import MPI

rank = MPI.COMM_WORLD.rank
size = MPI.COMM_WORLD.size
name = MPI.Get_processor_name()

print("process %d of %d on %s" % (rank, size, name))

