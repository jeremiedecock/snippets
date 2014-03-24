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

def grouper(flat_list, nested_list_size):
    nested_list = []
    for index in range(nested_list_size):
        nested_list_item = flat_list[index::nested_list_size]
        nested_list.append(nested_list_item)
    return nested_list


def flatten(nested_list):
    '''Flatten a list (eg. [[1,2,3],[4,5,6], [7], [8,9]] -> [1,2,3,4,5,6,7,8,9]).'''
    if nested_list is None:
        return None
    else:
        transposed_nested_list = list(itertools.izip_longest(*nested_list))  # transpose the 2d list (lines -> columns; columns -> lines)
        return [item for sublist in transposed_nested_list for item in sublist if item is not None]

###############################################################################

# INPUT

input_data = ['x' + str(i) for i in range(15)]
print "[1. input]", input_data

# MPI

comm = MPI.COMM_WORLD
size = comm.Get_size() # num proc
rank = comm.Get_rank() # proc id

if rank == 0:
    data = grouper(input_data, size)
else:
    data = None

# SCATTER

print "[2. before scatter] process", rank, ":", data

data = comm.scatter(data, root=0)

print "[3. after scatter] process", rank, ":", data

# PROCESS DATA

data = [(item, item.replace('x', 'result_of_x')) for item in data if item is not None]
#or simply:
#data = [item.replace('x', 'result_of_x') for item in data if item is not None]

# GATHER

print "[4. before gather] process", rank, ":", data

data = comm.gather(data, root=0)

print "[5. after gather] process", rank, ":", data

# OUTPUT

output_data = flatten(data)
print "[6. output]", output_data

