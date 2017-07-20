#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Display data as an image using pcolormesh (with given axis values)

One advantage of pcolormesh over imshow is that it is possible to give axis
values.
"""

import numpy as np
import matplotlib.pyplot as plt

# MAKE DATAS ##################################################################

x = np.arange(-3., 3., 0.01)
y = np.arange(-3., 3., 0.01)

xx, yy = np.meshgrid(x, y)

# The sphere function
zz = xx**2 + yy**2

# PLOT ########################################################################

fig, ax = plt.subplots()

im = ax.pcolormesh(xx, yy, zz)

plt.colorbar(im)              # draw the colorbar

# SAVE AND SHOW ###############################################################

plt.savefig("pcolormesh.png")
plt.show()
