#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://matplotlib.org/examples/mplot3d/surface3d_demo2.html

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

# Build datas ###############

u = np.linspace(0, 2.*np.pi, 100)
v = np.linspace(0, np.pi, 100)

x = 10 * np.outer(np.cos(u), np.sin(v))
y = 10 * np.outer(np.sin(u), np.sin(v))
z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

# Plot data #################

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(x, y, z, rstride=4, cstride=4)

ax.set_title("Parametric Sphere")

# SAVE FILES ######################

plt.savefig("parametric_sphere.png")
plt.show()

