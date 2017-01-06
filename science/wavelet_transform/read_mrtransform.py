#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt


def read_fits_file(file_path):
    # Open the FITS file
    hdu_list = fits.open(file_path)

    data = hdu_list[0].data

    # Close the FITS file
    hdu_list.close()

    return data


def save_image(data, file_path, quiet=False):
    interp='nearest'     # "raw" (non smooth) map

    fig = plt.figure()
    ax = fig.add_subplot(111)

    im = ax.imshow(data, interpolation=interp, origin='lower', cmap="gnuplot2")   # cmap=cm.inferno and cmap="inferno" are both valid

    plt.colorbar(im) # draw the colorbar

    plt.savefig(file_path)

    if not quiet:
        plt.show()


# PARSE OPTIONS ###############################################################

parser = argparse.ArgumentParser(description="Bspline wavelet transform")
parser.add_argument("filearg", nargs=1, metavar="FILE", help="the FITS file to process")
args = parser.parse_args()
file_path = args.filearg[0]

# PROCESS DATA ################################################################

# Read data
data = read_fits_file(file_path)

for scale_index, scale in enumerate(data):
    print(scale_index, scale.shape)

    # Write data
    output_file_path = file_path + ".mr." + str(scale_index) + ".png"
    save_image(scale, output_file_path, quiet=False)

