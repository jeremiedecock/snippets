#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)

# run:
#   mpirun -np 4 python scatter_gather_pickle_big_data.py | sort
#     or
#   mpiexec -n 4 python scatter_gather_pickle_big_data.py | sort

from mpi4py import MPI
import itertools
import math

###############################################################################

def grouper(iterable, num_items, fillvalue=None): # TODO
    '''Collect data into fixed-length chunks or blocks

    e.g. grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    See: http://stackoverflow.com/questions/10124751/convert-a-flat-list-to-list-of-list-in-python'''
    args = [iter(iterable)] * num_items
    return list(itertools.izip_longest(fillvalue=fillvalue, *args))


def flatten(l):
    '''Flatten a list (eg. [[1,2,3],[4,5,6], [7], [8,9]] -> [1,2,3,4,5,6,7,8,9]).'''
    if l is None:
        return None
    else:
        return [item for sublist in l for item in sublist]

###############################################################################

# INPUT

input_data = ['x' + str(i) for i in range(15)]
print "[1. input]", input_data

# MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    data_len = 16
    data = input_data
    num_item_per_proc = int(math.ceil(float(len(data)) / size)) # TODO
    data = grouper(data, num_item_per_proc)
else:
    data = None

# SCATTER

print "[2. before scatter] process", rank, ":", data

data = comm.scatter(data, root=0)

print "[3. after scatter] process", rank, ":", data

# PROCESS DATA

data = [item.replace('x', 'y') for item in data if item is not None]

# GATHER

print "[4. before gather] process", rank, ":", data

data = comm.gather(data, root=0)

print "[5. after gather] process", rank, ":", data

# OUTPUT

output_data = flatten(data)
print "[6. output]", output_data

