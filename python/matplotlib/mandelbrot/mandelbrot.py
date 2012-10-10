#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A Mandelbrot set demo"""

# Copyright (c) 2012 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

REAL_RANGE = np.arange(-2.0, 1.0, 0.05).tolist()
IMAG_RANGE = np.arange(-1.2, 1.2, 0.05).tolist()

EPSILON_MAX = 2.
NUM_IT_MAX = 32

Z_INIT = complex(0, 0)

def mandelbrot(x, y):
    it = 0
    z = Z_INIT
    c = complex(x, y)

    # Rem: abs(z) = |z| = math.sqrt(pow(z.imag,2) + pow(z.real,2))
    while it < NUM_IT_MAX and abs(z) <= EPSILON_MAX:
        z = pow(z, 2) + c
        it += 1

    # To print all levels
    return it

    ## To print only the level N
    #if it < N:
    #    return 1
    #else:
    #    return 0

def main():
    """Main function"""

    # Compute datas #############

    xgrid, ygrid = np.meshgrid(REAL_RANGE, IMAG_RANGE)

    data = np.array([mandelbrot(x, y) for y in IMAG_RANGE for x in REAL_RANGE]).reshape(len(IMAG_RANGE), len(REAL_RANGE))

    # Plot data #################

    fig = plt.figure()
    ax = axes3d.Axes3D(fig)

    # Plot mean surface

    ax.plot_surface(xgrid, ygrid, data, cmap=cm.jet, rstride=1, cstride=1, color='b', shade=True)

    # Title, etc.

    plt.title("Mandelbrot set")
    ax.set_xlabel("Re(c)")
    ax.set_ylabel("Im(c)")
    ax.set_zlabel("Color")

    plt.savefig("mandelbrot.png")

    plt.show()

if __name__ == '__main__':
    main()

