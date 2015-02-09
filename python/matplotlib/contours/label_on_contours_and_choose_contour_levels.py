#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# See http://matplotlib.org/api/axes_api.html?highlight=contour#matplotlib.axes.Axes.contour

import math
import numpy as np

import matplotlib
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def main():
    """The main function."""

    # Build data ################

    matplotlib.rcParams['xtick.direction'] = 'out'
    matplotlib.rcParams['ytick.direction'] = 'out'

    delta = 0.025
    x = np.arange(-3.0, 3.0, delta)
    y = np.arange(-2.0, 2.0, delta)
    X, Y = np.meshgrid(x, y)

    #Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
    #Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
    #Z = 10.0 * (Z2 - Z1)  # difference of Gaussians
    
    Z = X * np.exp(-X**2 - Y**2)


    # Plot data #################

    ## Plot contour
    #levels = np.arange(-1., 1., 0.1)
    #CS = plt.contour(Z, levels)           # Plot the levels specified in the "levels" variable
    #plt.clabel(CS, inline=1, fontsize=10)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Plot contour
    #levels = np.arange(-1., 1., 0.1)
    levels = np.array([-0.3, -0.25, -0.1, 0., 0.1, 0.3])
    CS = ax.contour(X, Y, Z, levels)           # Plot the levels specified in the "levels" variable
    ax.clabel(CS, inline=1, fontsize=10)

    plt.show()


if __name__ == '__main__':
    main()
