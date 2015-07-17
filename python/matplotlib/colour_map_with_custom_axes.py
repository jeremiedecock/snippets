#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: http://matplotlib.org/examples/pylab_examples/image_nonuniform.html

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import NonUniformImage
from matplotlib import cm

X_MIN=0
X_MAX=100
X_STEP=5

Y_MIN=0
Y_MAX=100
Y_STEP=5

# Fetch datas

x = np.arange(X_MIN, X_MAX, X_STEP)
y = np.arange(Y_MIN, Y_MAX, Y_STEP)
z_matrix = np.array([[xi * yi for xi in range(X_MIN, X_MAX, X_STEP)] for yi in range(Y_MIN, Y_MAX, Y_STEP)])

# Plot colour map

fig = plt.figure()
ax = fig.add_subplot(111)

#interp='nearest'     # "raw" (non smooth) map
interp = 'bilinear'   # "smooth" map

# NonUniformImage permet de definir la position des elements de 'z_matrix' sur les axes.
# Sans NonUniformImage, une matrice 'z_matrix' de taille (sx, sy) serait dessinee sur un repere avec un axe des abscisses allant de 0 a sx et un axe des ordonnees allant de 0 a sy.
im = NonUniformImage(ax, interpolation=interp, extent=(X_MIN, X_MAX, Y_MIN, Y_MAX), cmap=cm.binary)

# im.set_data(x, y, A)
#   Set the grid for the pixel centers, and the pixel values.
#   *x* and *y* are 1-D ndarrays of lengths N and M, respectively, specifying pixel centers
#   *A* is an (M,N) ndarray or masked array of values to be colormapped, or a (M,N,3) RGB array, or a (M,N,4) RGBA array.
im.set_data(x, y, z_matrix)

ax.images.append(im)
ax.set_xlim(X_MIN, X_MAX)
ax.set_ylim(Y_MIN, Y_MAX)

fig.colorbar(im) # draw colorbar

# SAVE FILES ######################
plt.savefig("colour_map_with_custom_axes.png")

plt.show()

