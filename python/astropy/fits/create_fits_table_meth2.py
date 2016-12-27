#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation:
# - http://docs.astropy.org/en/stable/table/index.html#astropy-table
# - http://docs.astropy.org/en/stable/io/unified.html#fits

from astropy.io import fits
from astropy.table import Table

OUTPUT_PATH = "out.fits"

# CREATE DATA #########################

a = [1, 4, 5]
b = [2.0, 5.0, 8.2]
c = ['x', 'y', 'z']

table = Table([a, b, c], names=('a', 'b', 'c'), meta={'name': 'first table'})

# SAVE THE FITS FILE ##################

table.write(OUTPUT_PATH, overwrite=True)
