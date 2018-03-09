#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plot 1 dimension data using a loglog scale
"""

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x = np.arange(1, 1000, 0.01)
y1 = x
y2 = np.sqrt(x)
y3 = x**2

# Plot data #################

fig = plt.figure(figsize=(8.0, 8.0))
ax = fig.add_subplot(111)

ax.loglog(x, y1, "-", label="x")
ax.loglog(x, y2, "-", label=r"$\sqrt{x}$")
ax.loglog(x, y3, "-", label=r"$x^2$")

# Set title and labels ######

ax.set_title(r"Loglog plot", fontsize=20)
ax.set_xlabel(r"$x$", fontsize=32)
ax.set_ylabel(r"$f(x)$", fontsize=32)

# Set legend ################

ax.legend(loc='lower right', fontsize=20)

# Save file #################

plt.savefig("plot_loglog.png")

# Plot ######################

plt.show()
