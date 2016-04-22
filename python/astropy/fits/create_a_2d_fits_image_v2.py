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

OUTPUT_PATH = "out.fits"

# CREATE DATA #########################

a = np.arange(255)
img = np.tile(a, (32, 1))

# CREATE THE FITS STRUCTURE ###########

hdu = fits.PrimaryHDU(img)

# SAVE THE FITS FILE ##################

if os.path.isfile(OUTPUT_PATH):
    os.remove(OUTPUT_PATH)

hdu.writeto(OUTPUT_PATH)

