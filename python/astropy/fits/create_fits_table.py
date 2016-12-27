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

a1 = np.array(['one', 'two', 'three'])
a2 = np.array([1, 2, 3])

col1 = fits.Column(name="col1", format="20A", array=a1)
col2 = fits.Column(name="col2", format="E",   array=a2)

cols = fits.ColDefs([col1, col2])

# CREATE THE FITS STRUCTURE ###########

table_hdu = fits.BinTableHDU.from_columns(cols)

# SAVE THE FITS FILE ##################

if os.path.isfile(OUTPUT_PATH):
    os.remove(OUTPUT_PATH)

table_hdu.writeto(OUTPUT_PATH)

