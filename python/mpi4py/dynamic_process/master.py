#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# run:
#   mpirun python3 master.py
#     or
#   mpiexec python3 master.py

from mpi4py import MPI
import sys

comm = MPI.COMM_SELF.Spawn(sys.executable, args=['worker.py'], maxprocs=5)

data = (1000, 2000, 3000)
data = comm.bcast(data, root=MPI.ROOT)

print("master:", data)

comm.Disconnect()
