#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make filled polygons between two curves
"""

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x = np.arange(0, 10, 0.05)
y1 = np.cos(x)
y2 = np.sin(x)

# Plot data #################

plt.plot(x, y1, x, y2)
plt.fill_between(x, y1, y2, facecolor='red', alpha=0.5)

# Save file and plot ########

plt.savefig("fill.png")
plt.show()
