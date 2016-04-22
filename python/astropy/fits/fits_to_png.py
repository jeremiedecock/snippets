#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation: http://docs.astropy.org/en/stable/io/fits/index.html

import argparse
from astropy.io import fits

import PIL.Image as pil_img # PIL.Image is a module not a class...
import numpy as np


# SAVE THE IMAGE ##############################################################

def save(img, output_file_path, min_val=None, max_val=None):
    """
    img is the image and it should be a 2D numpy array with values in the range [0,255].
    min_val and max_val are normalization parameters (the minimum and maximum value of a pixel).
    """

    if img.ndim != 2:
        raise Exception("The input image should be a 2D numpy array.")

    mode = "L"                           # "L" = grayscale mode
    pil_image = pil_img.new(mode, img.shape)

    # FLIP THE IMAGE IN THE UP/DOWN DIRECTION #############
    # WARNING: with fits, the (0,0) point is at the BOTTOM left corner
    #          whereas with pillow, the (0,0) point is at the TOP left corner
    #          thus the image should be converted

    img = np.flipud(img)

    # Normalize values ################
    # (FITS pixels value are unbounded but PNG pixels value are in range [0,255])
    if min_val == None:
        min_val = img.min()
    if max_val == None:
        max_val = img.max()

    img = img.astype(np.float64)
    img -= min_val
    img /= (max_val - min_val)
    img *= 255.
    img = img.astype(np.uint8)

    # Save ############################
    # WARNING: nested list and 2D numpy arrays are silently rejected!!!
    #          data *must* be a list or a 1D numpy array!
    pil_image.putdata(img.flatten())
    pil_image.save(output_file_path)


if __name__ == "__main__":

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Convert FITS files to PNG images")
    parser.add_argument("filearg", nargs=1, metavar="FILE", help="the FITS file to convert")
    args = parser.parse_args()
    file_path = args.filearg[0]

    # READ DATA ###############################################################

    # Open the FITS file
    hdu_list = fits.open(file_path)

    for hdu_index, hdu in enumerate(hdu_list):
        img = hdu.data   # "hdu.data" is a Numpy Array

        if img.ndim == 2:

            # If there are only one image (img is an 2D array)
            save(img, "out_hdu{}.png".format(hdu_index))

        elif img.ndim == 3:

            # If there is more than one image (img is an 3D array)
            for img_index, img in enumerate(img):
                save(img, "out_hdu{}_{}.png".format(hdu_index, img_index))

    # Close the FITS file
    hdu_list.close()

