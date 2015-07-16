#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

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

"""
Solving a linear program with cvxopt and Python 2.7.

min  x_2
s.t.
         x_1 + -x_2 <=  5
    -0.5 x_1 + -x_2 <= -4
      -2 x_1 + -x_2 <= -7

  c = (0  1)
  
  A = ⎛   1  -1⎞
      ⎜-0.5  -1⎟
      ⎝  -2  -1⎠
  
  b = ⎛ 5⎞
      ⎜-4⎟
      ⎝-7⎠

The expected optimal solution is:

  x* = ⎛6⎞ 
       ⎝1⎠

See http://http://cvxopt.org/examples/tutorial/lp.html
and http://cvxopt.org/examples/tutorial/numpy.html
"""

import cvxopt
import cvxopt.solvers

# Or:
# from cvxopt import matrix, solvers

import numpy as np

def main():

    np_c = np.array([ 0., 1. ])
    np_A = np.array([ [ 1.0, -1.0],
                      [-0.5, -1.0],
                      [-2.0, -1.0] ])
    np_b = np.array([ 5., -4., -7. ])

    c = cvxopt.matrix(np_c)
    A = cvxopt.matrix(np_A)
    b = cvxopt.matrix(np_b)

    sol = cvxopt.solvers.lp(c, A, b)

    x_star = sol['x']
    np_x_star = np.array(x_star)

    print('x* = ')
    print(np_x_star)
    
    print(sol)

if __name__ == '__main__':
    main()
