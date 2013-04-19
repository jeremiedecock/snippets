# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

__all__ = ['Optimizer', 'Log']

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import warnings

class Optimizer:

    def __init__(self):
        self.log = Log()

    def plotSamples(self, x, y):

        assert x.ndim == 2, x.ndim
        assert y.ndim == 2, y.ndim
        assert y.shape[1] == 1, y.shape

        if x.shape[1]==1:
            # 1D case
            plt.plot(x[:,0], y, ".")
            
            x_min = x[y.argmin(), :]
            y_min = y.min()
            plt.plot(x_min, y_min, ".r")

            plt.show()
        elif x.shape[1]==2:
            # 2D case
            fig = plt.figure()
            ax = axes3d.Axes3D(fig)
            ax.scatter(x[:,0], x[:,1], y, color='b')
            
            x_min = x[y.argmin(), :]
            y_min = y.min()
            ax.scatter(x_min[0], x_min[1],  y_min, color='r')

            plt.show()
        else:
            warnings.warn("Cannot plot samples: too many dimensions.")

    def plotCosts(self, y):

        assert y.shape[1]==1

        plt.plot(y)
        plt.show()

class Log:
    def __init__(self):
        self.data = {}
