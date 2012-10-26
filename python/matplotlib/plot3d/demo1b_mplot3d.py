#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import math

# Build datas ###############

x = np.arange(-5, 5, 0.25)
y = np.arange(-5, 5, 0.25)

xx,yy = np.meshgrid(x, y)

z = np.zeros(xx.shape)

for xi in range(z.shape[0]):
    for yi in range(z.shape[1]):
        z[xi, yi] = math.sin(math.sqrt(xx[xi, yi]**2 + yy[xi, yi]**2))

# Plot data #################

fig = plt.figure()
ax = axes3d.Axes3D(fig)
ax.plot_wireframe(xx, yy, z)

plt.show()

