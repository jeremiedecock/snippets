#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

width = 0.4       # the width of the bars

x = np.arange(-5, 6)
y1 = np.power(x, 2)
y2 = np.power(x, 3)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.bar(x, y1, width, color='r')
ax.bar(x+width, y2, width, color='b')

plt.show()
