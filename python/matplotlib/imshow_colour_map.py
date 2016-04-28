#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: http://matplotlib.org/examples/pylab_examples/image_demo.html

# See also:
# - http://matplotlib.org/examples/color/colormaps_reference.html (the list of all colormaps)
# - http://matplotlib.org/users/colormaps.html?highlight=colormap#mycarta-banding (what is the right colormap to choose for a given plot)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# Fetch datas

z_matrix = np.array([[xi * yi for xi in range(50)] for yi in range(50)])

# Plot colour map

#interp='nearest'     # "raw" (non smooth) map
interp = 'bilinear'   # "smooth" map

# The list of all colormaps: http://matplotlib.org/examples/color/colormaps_reference.html
plt.imshow(z_matrix, interpolation=interp, origin='lower', cmap="inferno")   # You can use cmap=cm.inferno or cmap="inferno"
#plt.imshow(z_matrix, interpolation=interp, origin='lower', cmap=cm.inferno) # You can use cmap=cm.inferno or cmap="inferno"

plt.colorbar() # draw colorbar

# SAVE FILES ######################
plt.savefig("colour_map.png")

plt.show()

