#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

delta = 0.025
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)

Z = X * np.exp(-X**2 - Y**2)

# Plot data #################

fig, ax = plt.subplots()

max_value = np.max(Z)
levels = np.array([0.1*max_value, 0.3*max_value, 0.6*max_value])

cs = plt.contour(x, y, Z, levels,
                 linewidths=(2, 2, 3), linestyles=('dotted', 'dashed', 'solid'),
                 alpha=0.5, colors='blue', label="TC")
ax.clabel(cs, inline=False, fontsize=12)

# Set title and labels ######

ax.set_title("Contour", fontsize=20)
ax.set_xlabel(r"$X_1$", fontsize=20)
ax.set_ylabel(r"$X_2$", fontsize=20)

# Set legend ################

lines = [ cs.collections[0]]
labels = ['X']
ax.legend(lines, labels, prop={'size': 14}, loc='best', fancybox=True, framealpha=0.5)

# Save file #################

plt.savefig("contour.png")

# Plot ######################

plt.show()
