#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation: http://docs.astropy.org/en/stable/io/fits/index.html

import os.path

import argparse
from astropy.io import fits

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


# PARSE OPTIONS ###############################################################

parser = argparse.ArgumentParser(description="Convert FITS files to PNG images")

parser.add_argument("filearg", nargs=1, metavar="FILE", help="the FITS file to convert")

args = parser.parse_args()

file_path = args.filearg[0]


# READ DATA ###################################################################

# Open the FITS file
hdu_list = fits.open(file_path)

# Print the content of the FITS file (HDU headers)
for hdu_id, hdu in enumerate(hdu_list):
    data = hdu.data   # "hdu.data" is a Numpy Array

    if data.ndim == 2:
        # If there are only one image (data is an 2D array)
        fig = plt.figure(figsize=(8.0, 8.0))
        ax = fig.add_subplot(111)
        ax.imshow(data, interpolation='nearest', cmap=cm.gray)
        plt.savefig("{}_hdu{}.png".format(os.path.splitext(file_path)[0], hdu_id))
    elif data.ndim == 3:
        # If there is more than one image (data is an 3D array)
        for img_index, img in enumerate(data):
            fig = plt.figure(figsize=(8.0, 8.0))
            ax = fig.add_subplot(111)
            ax.imshow(img, interpolation='nearest', cmap=cm.gray)
            plt.savefig("HDU{}_{}.png".format(hdu_id, img_index))

# Close the FITS file
hdu_list.close()

