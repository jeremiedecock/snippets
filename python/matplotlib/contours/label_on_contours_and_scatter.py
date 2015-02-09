#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

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

    ## difference of Gaussians
    #Z = 10.0 * (Z2 - Z1)

    Z = X * np.exp(-X**2 - Y**2)


    # Plot data #################

    ## Contours and labels
    #CS = plt.contour(X, Y, Z)
    #plt.clabel(CS, inline=1, fontsize=10)

    ## Heat map
    ##im = plt.imshow(Z, interpolation='bilinear', origin='lower', cmap=cm.gray, extent=(-3,3,-2,2))

    ## Scatter
    #x = np.array([1, 0.5, 2])
    #y = np.array([1, 0.5, 2])
    #plt.scatter(x, y, marker='o', c='b', s=5, zorder=10)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # Contours and labels
    CS = ax.contour(X, Y, Z)
    ax.clabel(CS, inline=1, fontsize=10)

    # Heat map
    #im = ax.imshow(Z, interpolation='bilinear', origin='lower', cmap=cm.gray, extent=(-3,3,-2,2))

    # Scatter
    x = np.array([1, 0.5, 2])
    y = np.array([1, 0.5, 2])
    ax.scatter(x, y, marker='o', c='b', s=5, zorder=10)

    plt.show()


if __name__ == '__main__':
    main()
