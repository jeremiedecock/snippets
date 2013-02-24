#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

# Build datas ###############

num_points = 1000
mu = np.array([0., 2.5, 5.])
cov = np.array([[1., 0., 0.],
                [0., 2., 0.],
                [0., 0., 3.]])

x = np.random.multivariate_normal(mu, cov, num_points)

# Plot data #################

fig = plt.figure()
ax = axes3d.Axes3D(fig)
ax.scatter(x[:,0], x[:,1], x[:,2], color='b')

ax.set_xlim(-5., 10.)
ax.set_ylim(-5., 10.)
ax.set_zlim(-5., 10.)

plt.show()

