#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# run:
#   mpirun python3 pi_master.py
#     or
#   mpiexec python3 pi_master.py

from mpi4py import MPI
import sys

comm = MPI.COMM_SELF.Spawn(sys.executable, args=['pi_worker.py'], maxprocs=5)

data = 100
comm.bcast(data, root=MPI.ROOT)

result = comm.reduce(None, op=MPI.SUM, root=MPI.ROOT)

print(result)

comm.Disconnect()
