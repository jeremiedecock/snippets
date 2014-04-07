#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)

# run:
#   mpirun -np 4 python scatter_gather_pickle_big_data_iterative.py | sort
#     or
#   mpiexec -n 4 python scatter_gather_pickle_big_data_iterative.py | sort

from mpi4py import MPI
import itertools

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


def process_data(data):
    res = [(item, item.replace('x', 'result_of_x')) for item in data if item is not None]
    #or simply:
    #res = [item.replace('x', 'result_of_x') for item in data if item is not None]
    return res


###############################################################################

# MPI

comm = MPI.COMM_WORLD
size = comm.Get_size() # num proc
rank = comm.Get_rank() # proc id

if rank == 0:
    output_res = {}

for iteration_index in range(3):

    # INPUT

    if rank == 0:
        input_data = ['x' + str(iteration_index) + '.' + str(i) for i in range(15)]
        print "[" + str(iteration_index) + ".1 input]", input_data

        data = grouper(input_data, size)
    else:
        data = None

    # SCATTER

    print "[" + str(iteration_index) + ".2 before scatter] process", rank, ":", data

    data = comm.scatter(data, root=0)

    print "[" + str(iteration_index) + ".3 after scatter] process", rank, ":", data

    # PROCESS DATA

    res = process_data(data)

    # GATHER

    print "[" + str(iteration_index) + ".4 before gather] process", rank, ":", res

    res = comm.gather(res, root=0)

    print "[" + str(iteration_index) + ".5 after gather] process", rank, ":", res

    # OUTPUT

    if rank == 0:
        output_res[iteration_index] = flatten(res)
        print "[" + str(iteration_index) + ".6 output]", output_res[iteration_index]

if rank == 0:
    print "[output]", output_res

