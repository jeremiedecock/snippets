#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enthought.mayavi import mlab
import numpy as np

# Build datas ###############

x = np.arange(-5, 5, 0.25)
y = np.arange(-5, 5, 0.25)
x,y = np.meshgrid(x, y)
#x,y = np.mgrid[-5:5, -5:5]

r = np.sqrt(x**2 + y**2)
z = np.sin(r)

# Plot data #################

s = mlab.mesh(x, y, z)
#s = mlab.surf(z)

mlab.show()

