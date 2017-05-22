#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make plots using using the *seaborn-poster* style
"""

# See: http://matplotlib.org/users/style_sheets.html

import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-poster')  # <- SETUP STYLE

# Build datas ###############

x = np.arange(-10, 10, 0.01)
y = np.sin(2. * 2. * np.pi * x) * 1. / np.sqrt(2. * np.pi) * np.exp(-(x**2.)/2.)

# Plot data #################

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(x, y, "-", label="Test")

# Set title and labels ######

ax.set_title("Test")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")

# Set legend ################

ax.legend(loc='lower right')

# Save file #################

plt.savefig("plot_style_seaborn_poster.png")

# Plot ######################

plt.show()
