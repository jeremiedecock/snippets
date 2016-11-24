#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation:
# - http://docs.astropy.org/en/stable/io/fits/
# - http://docs.astropy.org/en/stable/io/fits/api/files.html
# - http://www.astropy.org/astropy-tutorials/FITS-tables.html
# - http://www.astropy.org/astropy-tutorials/FITS-images.html
# - http://www.astropy.org/astropy-tutorials/FITS-header.html

import argparse
from astropy.io import fits
from astropy.table import Table

# PARSE OPTIONS ###############################################################

parser = argparse.ArgumentParser(description="An astropy snippet")
parser.add_argument("filearg", nargs=1, metavar="FILE", help="the FITS file to process")
args = parser.parse_args()
file_path = args.filearg[0]

# PRINT GENERAL HDU INFOS #####################################################

print()
print(80 * '*')
print()
fits.info(file_path)
print()
print(80 * '*')
print()

# READ DATA ###################################################################


# Open the FITS file
table = Table.read(file_path)

print(table)
print()
print(type(table))
