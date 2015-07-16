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
               -x_2 <= -3
      -2 x_1 + -x_2 <= -7

  c = (0  1)
  
  A = ⎛   1  -1⎞
      ⎜   0  -1⎟
      ⎝  -2  -1⎠
  
  b = ⎛ 5⎞
      ⎜-3⎟
      ⎝-7⎠

The expected optimal solution is:

  x* = ⎛2⎞ 
       ⎝3⎠

to

  x* = ⎛8⎞ 
       ⎝3⎠

See http://http://cvxopt.org/examples/tutorial/lp.html
and http://http://cvxopt.org/examples/tutorial/creating-matrices.html
"""

import cvxopt
import cvxopt.solvers

# Or:
# from cvxopt import matrix, solvers

def main():

    # Cvxopt doesn't use the same definition notation than numpy.
    # Each inner list represents a *column* of the matrix, not a row !
    # The following matrix
    #
    #  A = ⎛   1  -1⎞
    #      ⎜   0  -1⎟
    #      ⎝  -2  -1⎠
    #
    # is defined
    #
    #  cvxopt.matrix([ [ 1.0,  0.0, -2.0],
    #                  [-1.0, -1.0, -1.0] ])

    c = cvxopt.matrix([ 0., 1. ])
    A = cvxopt.matrix([ [ 1.0,  0.0, -2.0],
                        [-1.0, -1.0, -1.0] ])
    b = cvxopt.matrix([ 5., -3., -7. ])

    # By default, cvxopt *minimize* the objective function.
    sol = cvxopt.solvers.lp(c, A, b)

    print('x* = ')
    print(sol['x'])
    
    print(sol)

if __name__ == '__main__':
    main()
