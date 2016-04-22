#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation: http://docs.astropy.org/en/stable/io/fits/index.html

import argparse
from astropy.io import fits

import PIL.Image as pil_img # PIL.Image is a module not a class...
import numpy as np
import os


# SAVE THE IMAGE ##############################################################

def save(img, output_file_path):
    """
    img is the image and it should be a 2D numpy array with values in the range [0,255].
    """

    mode = "L"                           # "L" = grayscale mode
    pil_image = pil_img.new(mode, img.shape)

    # FLIP THE IMAGE IN THE UP/DOWN DIRECTION #############
    # WARNING: with fits, the (0,0) point is at the BOTTOM left corner
    #          whereas with pillow, the (0,0) point is at the TOP left corner
    #          thus the image should be converted

    img = np.flipud(img)

    # CREATE THE FITS STRUCTURE ###########################

    hdu = fits.PrimaryHDU(img)

    # SAVE THE FITS FILE ##################################

    if os.path.isfile(output_file_path):
        os.remove(output_file_path)

    hdu.writeto(output_file_path)


if __name__ == "__main__":

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Convert FITS files to PNG images")
    parser.add_argument("filearg", nargs=1, metavar="FILE", help="the FITS file to convert")
    args = parser.parse_args()
    input_file_path = args.filearg[0]

    # READ AND SAVE DATA ######################################################

    img = np.array(pil_img.open(input_file_path).convert('L'))  # img is a 2D numpy array
    save(img, "out.fits")

