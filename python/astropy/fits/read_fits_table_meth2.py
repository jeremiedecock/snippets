#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation:
# - http://docs.astropy.org/en/stable/table/index.html#astropy-table
# - http://docs.astropy.org/en/stable/io/unified.html#fits

import argparse
from astropy.table import Table

# PARSE OPTIONS ###############################################################

parser = argparse.ArgumentParser(description="An astropy snippet")
parser.add_argument("filearg", nargs=1, metavar="FILE", help="the FITS file to process")
args = parser.parse_args()
file_path = args.filearg[0]

# READ DATA ###################################################################


# Open the FITS file
table = Table.read(file_path)

print(table)
print()
print(type(table))
