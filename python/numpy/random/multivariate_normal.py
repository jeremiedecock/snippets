#!/usr/bin/env python
# -*- coding: utf-8 -*-
            
import math 
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d


mu = np.array([0., 0.])
cov = np.array([[1., 0.],
                [1., 1.]])
num_points = 10000

x = np.random.multivariate_normal(mu, cov, num_points)

plt.plot(x[:,0], x[:,1], ".")

plt.xlim(-5, 5)
plt.ylim(-5, 5)

plt.show()

