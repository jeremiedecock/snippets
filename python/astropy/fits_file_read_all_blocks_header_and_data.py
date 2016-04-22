#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation: http://docs.astropy.org/en/stable/io/fits/index.html

import argparse
from astropy.io import fits


# PARSE OPTIONS ###############################################################

parser = argparse.ArgumentParser(description="An astropy snippet")

parser.add_argument("filearg", nargs=1, metavar="FILE", help="the FITS file to process")

args = parser.parse_args()

file_path = args.filearg[0]


# READ DATA ###################################################################

# Open the FITS file
hdu_list = fits.open(file_path)

# Print the content of the FITS file (HDU headers)
hdu_list.info()

print("---")

for hdu_id, hdu in enumerate(hdu_list):
    print("HDU {}".format(hdu_id))

    header = hdu.header
    for key, value in header.items():
        print(key, ":", value)

    data = hdu.data   # "hdu.data" is a Numpy Array
    print(data)
    print(data.shape)

    print("---")

# Close the FITS file
hdu_list.close()

