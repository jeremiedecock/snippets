#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A bifurcation diagram demo: Feigenbaum Constant
See http://fr.wikipedia.org/wiki/Nombres_de_Feigenbaum"""

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

MU_MIN = 2.7
MU_MAX = 4.0
MU_DELTA = 0.005

NUM_IT = 200

X_INIT = 0.5

def main():
    """Main function"""

    x = X_INIT
    y_list = []

    for mu in np.arange(MU_MIN, MU_MAX, MU_DELTA).tolist():
        y = []
        for it in range(NUM_IT):
            x = mu * x * (1.0 - x)
            y.append(x)
        y_list.append(y)

    plt.plot(y_list, ',')
    plt.xlabel('$\mu$')
    plt.ylabel('$x$')
    plt.show()

if __name__ == '__main__':
    main()
