#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

# Build datas ###############

x = np.arange(-5, 5, 0.25)
y = np.arange(-5, 5, 0.25)

xx,yy = np.meshgrid(x, y)
z = np.sin(np.sqrt(xx**2 + yy**2))

# Plot data #################

fig = plt.figure()
ax = axes3d.Axes3D(fig)
ax.plot_wireframe(xx, yy, z)

# SAVE FILES ######################
plt.savefig("demo1_mplot3d.png")

plt.show()

