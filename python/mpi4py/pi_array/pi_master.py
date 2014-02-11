#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# run:
#   mpirun python pi_master.py
#     or
#   mpiexec python pi_master.py

from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_SELF.Spawn(sys.executable, args=['pi_worker.py'], maxprocs=5)

data = np.array(100, 'i')  # [100]
comm.Bcast([data, MPI.INT], root=MPI.ROOT)

result = np.array(0.0, 'd')
comm.Reduce(None, [result, MPI.DOUBLE], op=MPI.SUM, root=MPI.ROOT)

print(result)

comm.Disconnect()
