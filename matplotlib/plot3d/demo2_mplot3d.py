#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

POPULATION_SIZE=1000.  # Num. simulations

a = np.loadtxt("demo2.dat")

x = a[:,0]
y = a[:,1]
z = a[:,6]    # reward (mean value)
zerr = a[:,7] # reward (standard deviation)
zconf = 2. * a[:,7] / math.sqrt(POPULATION_SIZE) # confidence interval ~95%

# Build datas ###############

#xgrid = x.reshape(len(np.unique(x)), len(np.unique(y)))
#ygrid = y.reshape(len(np.unique(x)), len(np.unique(y)))
zgrid = z.reshape(len(np.unique(x)), len(np.unique(y)))

xgrid, ygrid = np.meshgrid(np.unique(x), np.unique(x))

print zgrid

# Plot data #################

fig = plt.figure()
ax = axes3d.Axes3D(fig)

# Plot mean surface

#ax.plot_wireframe(xgrid, ygrid, zgrid)
#ax.plot_surface(xgrid, ygrid, zgrid, rstride=1, cstride=1, color='b', shade=True)
#ax.plot_surface(xgrid, ygrid, zgrid, cmap=cm.jet, rstride=1, cstride=1, color='b', shade=True)
surf = ax.plot_surface(xgrid, ygrid, zgrid, cmap=cm.jet, rstride=1, cstride=1, color='b', shade=True)

# Plot errorbars (standard deviation)

#for i in np.arange(0, len(zerr)):
#    ax.plot([y[i], y[i]], [x[i], x[i]], [z[i]+zerr[i], z[i]-zerr[i]], marker="_", color='k')

# Plot errorbars (confidence interval 95%)

for i in np.arange(0, len(zconf)):
    ax.plot([y[i], y[i]], [x[i], x[i]], [z[i]+zconf[i], z[i]-zconf[i]], marker="_", color='k')

# Title, etc.

plt.title("demo2")
ax.set_xlabel("label_x")
ax.set_ylabel("label_y")
ax.set_zlabel("label_z")

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.savefig("demo2.png")

plt.show()
