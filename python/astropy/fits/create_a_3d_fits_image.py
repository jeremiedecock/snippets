#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation:
# - http://docs.astropy.org/en/stable/io/fits/
# - http://docs.astropy.org/en/stable/io/fits/api/files.html
# - http://www.astropy.org/astropy-tutorials/FITS-tables.html
# - http://www.astropy.org/astropy-tutorials/FITS-images.html
# - http://www.astropy.org/astropy-tutorials/FITS-header.html

import os.path

from astropy.io import fits
import numpy as np

from mpl_toolkits.mplot3d import axes3d

OUTPUT_PATH = "out.fits"

# CREATE DATA #########################

X1, Y1, Z1 = axes3d.get_test_data(0.05)
X2, Y2, Z2 = axes3d.get_test_data(0.05)
X3, Y3, Z3 = axes3d.get_test_data(0.05)

Z1 *= 1.
Z2 *= -1.
Z3 *= 2.

img = np.stack([Z1, Z2, Z3], 0)

print("Image shape:", img.shape)

# CREATE THE FITS STRUCTURE ###########

hdu = fits.PrimaryHDU(img)

# SAVE THE FITS FILE ##################

if os.path.isfile(OUTPUT_PATH):
    os.remove(OUTPUT_PATH)

hdu.writeto(OUTPUT_PATH)

