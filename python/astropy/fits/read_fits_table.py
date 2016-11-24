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
hdu_list = fits.open(file_path)

# For each blocks
for hdu_index, hdu in enumerate(hdu_list):

    print("HDU {}".format(hdu_index), 40 * '*')
    print()

    # Print header
    print("* HEADERS")
    print()
    header = hdu.header
    for key, value in header.items():
        print(key, ":", value)
    print()

    # Print columns
    if not hdu.is_image:
        print("* COLUMNS")
        print()
        columns = hdu.columns
        print(columns)

        print()
        print(columns.names)

        print()
        columns.info()
        print()

    # Print data
    print("* DATA")
    print()
    data = hdu.data   # "hdu.data" is a Numpy Array
    print(data)
    print()

# Close the FITS file
hdu_list.close()

