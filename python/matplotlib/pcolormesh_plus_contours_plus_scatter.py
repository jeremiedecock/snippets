#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Display data as an image using pcolormesh and contours plus plot points with
scatter.

One advantage of pcolormesh over imshow is that it is possible to give axis
values.
"""

import numpy as np
import matplotlib.pyplot as plt

# MAKE DATAS ##################################################################

x = np.arange(-3., 3., 0.05)
y = np.arange(-3., 3., 0.05)

xx, yy = np.meshgrid(x, y)

# The sphere function
zz = xx**2 + yy**2

# PLOT BACKGROUND LEVEL #######################################################

fig, ax = plt.subplots()

im = ax.pcolormesh(xx, yy, zz)

plt.colorbar(im)              # draw the colorbar

# PLOT ########################################################################

max_value = np.max(zz)
levels = np.array([0.1*max_value, 0.3*max_value, 0.6*max_value])

cs = plt.contour(xx, yy, zz, levels,
                         linewidths=(2, 2, 3), linestyles=('dotted', 'dashed', 'solid'),
                                          alpha=0.5, colors='blue')
ax.clabel(cs, inline=False, fontsize=12)

# PLOT ########################################################################

ax.scatter(0, 0, c='red', label="$x^*$")

ax.legend(fontsize=12);

# SAVE AND SHOW ###############################################################

plt.savefig("pcolormesh_plus_contours_plus_scatter.png")
plt.show()
