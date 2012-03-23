#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

# Build datas ###############

x = np.arange(-5, 5, 0.25)
y = np.arange(-5, 5, 0.25)
x,y = np.meshgrid(x, y)
#x,y = np.mgrid[-5:5, -5:5]

r = np.sqrt(x**2 + y**2)
z = np.sin(r)

# Plot data #################

fig = plt.figure()
ax = axes3d.Axes3D(fig)
ax.plot_wireframe(x, y, z)

plt.show()

