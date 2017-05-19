#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make a bar plot with rectangles
"""

import numpy as np
import matplotlib.pyplot as plt

WIDTH = 0.4       # the width of the bars

# Build datas ###############

x = np.arange(-5, 6)
y1 = np.power(x, 2)
y2 = np.power(x, 3)

# Plot data #################

fig = plt.figure()
ax = fig.add_subplot(111)

ax.bar(x, y1, WIDTH, color='r')
ax.bar(x + WIDTH, y2, WIDTH, color='b')

# Save file and plot ########

plt.savefig("bar.png")
plt.show()
