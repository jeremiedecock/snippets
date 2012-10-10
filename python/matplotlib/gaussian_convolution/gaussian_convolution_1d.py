#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Gaussian convolution 1D"""

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

SIGMA = 0.5

def d_square(x, xarray):
    """Computes the squared euclidian distance between x and xarray values."""

    #d = np.sum(np.power(x - xarray, 2), 1) # if x is a vector
    d = np.power(x - xarray, 2)
    return d


def estimate(x, x_known, y_known, sigma):
    """Estimates the value y of x, knowing x_known and y_known sets."""

    d = d_square(x, x_known)
    e = np.exp( -1. / pow(sigma, 2) * d )

    term1 = np.sum(e * y_known)
    term2 = np.sum(e)               # to normalize "term1"

    y_hat = term1 / term2

    #return y_hat
    return y_hat, term1, term2      # uncomment this line to see term1 and term2


def main():
    """Main function"""

    # Known points
    x_known = np.array([-3., -2., -1., 0., 1., 2.])
    x_known = np.array([-3., -2., -1.1, -1., 0., 1., 2.])
    y_known = np.array([-1., -2.,  1.2,  1., 4., 3., 2.])

    # Points to approximate
    x_test = np.arange(-5., 5., 0.05).tolist()
    y_test = np.array([estimate(x, x_known, y_known, SIGMA) for x in x_test])

    # Plot
    plt.plot(x_known, y_known, 'r*')
    plt.plot(x_test, y_test)
    plt.xlabel('$x$')
    plt.ylabel('$\hat{y}$')
    plt.show()

if __name__ == '__main__':
    main()
