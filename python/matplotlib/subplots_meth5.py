#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

"""
Make subplots (alternative method 5)
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-10, 10, 0.1)

y_array_list = [np.cos(x),
                np.sin(x),
                np.tan(x),
                np.cosh(x),
                np.sinh(x),
                np.tanh(x)]

title_list = [r"$\cos(x)$",
              r"$\sin(x)$",
              r"$\tan(x)$",
              r"$\cosh(x)$",
              r"$\sinh(x)$",
              r"$\tanh(x)$"]

fig, axis_array = plt.subplots(nrows=2,
                               ncols=3,
                               squeeze=False,   # <- Always make a 2D array, whatever nrows and ncols
                               figsize=(9, 6))

axis_array = axis_array.flat

for (axis, y, title) in zip(axis_array, y_array_list, title_list):
    axis.plot(x, y)
    axis.set_title(title)

plt.show()

