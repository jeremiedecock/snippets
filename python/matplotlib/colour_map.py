#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: http://matplotlib.org/examples/pylab_examples/image_demo.html

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# Fetch datas

z_matrix = np.array([[xi * yi for xi in range(50)] for yi in range(50)])

# Plot colour map

#interp='nearest'     # "raw" (non smooth) map
interp = 'bilinear'   # "smooth" map

plt.imshow(z_matrix, interpolation=interp, origin='lower') #, cmap=cm.binary)

plt.colorbar() # draw colorbar

# SAVE FILES ######################
plt.savefig("colour_map.png")

plt.show()

