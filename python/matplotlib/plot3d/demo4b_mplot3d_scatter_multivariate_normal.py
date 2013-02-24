#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

# Build datas ###############

num_points = 1000
mu = np.array([0., 0., 0.])
cov = np.array([[1., 0., 0.],
                [0., 1., 0.],
                [0., 0., 1.]])

x = np.random.multivariate_normal(mu, cov, num_points)

# Plot data #################

fig = plt.figure()
ax = axes3d.Axes3D(fig)
ax.scatter(x[:,0], x[:,1], x[:,2], color='b')

plt.show()

