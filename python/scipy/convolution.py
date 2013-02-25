#!/usr/bin/env python
# -*- coding: utf-8 -*-
            
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt

# The imput signal x
x = np.zeros(100)
x[30:60] = 1.

# ...
y = np.ones(30)

xc = scipy.signal.convolve(x, y)

plt.plot(x)
plt.plot(xc / 30.)
plt.show()

