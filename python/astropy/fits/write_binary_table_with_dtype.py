#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation:
# - http://docs.astropy.org/en/stable/table/index.html#getting-started
# - http://www.astropy.org/astropy-tutorials/FITS-tables.html
# - http://www.astropy.org/astropy-tutorials/FITS-header.html

import argparse
from astropy.io import fits

import numpy as np
import astropy.table

# PARSE OPTIONS ###############################################################

parser = argparse.ArgumentParser(description="An astropy snippet")
parser.add_argument("filearg", nargs=1, metavar="FILE", help="the output FITS file")
args = parser.parse_args()
file_path = args.filearg[0]

# WRITE DATA ##################################################################

name_list = ("column1", "column2", "column3")
dtype_list = ("S128",  # column1 -> 128 bytes string
              "i4",    # column2 -> 4 bytes integer
              "f8")    # column3 -> 8 bytes float

table = astropy.table.Table(names=name_list,
                            dtype=dtype_list)

table.add_row(["A", 1, 1.1])
table.add_row(["B", 2, 2.2])
table.add_row(["C", 3, 3.3])

print(table)

table.write(file_path, overwrite=True)
