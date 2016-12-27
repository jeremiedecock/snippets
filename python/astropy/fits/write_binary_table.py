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

table = astropy.table.Table(names=("column1", "column2", "column3"))

table.add_row([1, 2, 3])
table.add_row([10, 20, 30])
table.add_row([100, 200, 300])

print(table)

table.write(file_path, overwrite=True)
