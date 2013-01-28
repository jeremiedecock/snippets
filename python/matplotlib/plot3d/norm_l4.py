#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

N = 4.

# Build datas ###############

x = np.arange(-5, 5, 0.1)
y = np.arange(-5, 5, 0.1)

xx,yy = np.meshgrid(x, y)
z = np.power(np.power(xx, N) + np.power(yy, N), 1./N)

# Plot data #################

fig = plt.figure()

#ax = axes3d.Axes3D(fig)
#ax.plot_wireframe(xx, yy, z)

ax = fig.gca(projection='3d')

ax.plot_surface(xx, yy, z, rstride=5, cstride=5, alpha=0.3)
cset = ax.contourf(xx, yy, z, zdir='z', offset=0, cmap=cm.coolwarm)

ax.set_xlabel(r'$x_1$')
ax.set_ylabel(r'$x_2$')
ax.set_zlabel(r'$||x||_{4}$')

plt.show()

