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

import numpy as np
import matplotlib.pyplot as plt

# PARSE OPTIONS ###############################################################

parser = argparse.ArgumentParser(description="An astropy snippet")
parser.add_argument("filearg", nargs=1, metavar="FILE", help="the FITS file to read")
args = parser.parse_args()
file_path = args.filearg[0]

# READ DATA ###################################################################

# Open the FITS file
hdu_list = fits.open(file_path)

# For each blocks
for hdu_index, hdu in enumerate(hdu_list):
    print("HDU {}".format(hdu_index))

    # Print header
    header = hdu.header
    for key, value in header.items():
        print(key, ":", value)

    # Print data
    try:
        data = hdu.data   # "hdu.data" is a Numpy Array
        print(data)
        print(type(data))
        print(data.shape)
    except:
        pass

    print("---")

    # GET DATA FROM ONE GIVEN COLUMN EXAMPLE ##############

    # Print column named "column1" of hdu1 (if it exist)
    # See './write_binary_tqble.py'
    if hdu_index == 1:
        try:
            print(hdu.data['column1'])

            #plt.plot(hdu.data['column1'])
            #plt.show()
        except:
            pass

# Close the FITS file
hdu_list.close()

