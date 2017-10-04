#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plot an horizontal line
"""

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x = np.arange(-10, 10, 0.01)
y = x**2

# Plot data #################

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)

ax.plot(x, y, "-k", alpha=0.25)
ax.axhline(50)

# Save file #################

plt.savefig("horizontal_line.png")

# Plot ######################

plt.show()
