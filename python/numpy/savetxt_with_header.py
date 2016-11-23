#!/usr/bin/env python

import numpy as np

def save_np_array(output_file_path, data_array, header_list):

    np.savetxt(output_file_path,
               data_array,
               #fmt="%10.5f",
               #delimiter=" ",
               header="; ".join(header_list),
               #comments="# "                 # String that will be prepended to the ``header`` and ``footer`` strings, to mark them as comments. Default: '# '.
               )


data = np.random.rand(10, 4)
header = ["rand 1", "rand 2", "rand 3", "rand 4"]

save_np_array("test.dat", data, header)
