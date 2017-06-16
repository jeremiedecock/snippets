#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hand drawn like style
"""

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x = np.arange(-10, 10, 0.01)
y = np.sin(2. * 2. * np.pi * x) * 1. / np.sqrt(2. * np.pi) * np.exp(-(x**2.)/2.)

# Plot data #################

with plt.xkcd():                        # <- Set XKCD style
    fig = plt.figure(figsize=(6., 6.))
    ax = fig.add_subplot(111)

    ax.plot(x, y, "-", label="Test")

    # Set title and labels ######

    ax.set_title(r"Test", fontsize=20)
    ax.set_xlabel(r"$x$", fontsize=32)
    ax.set_ylabel(r"$f(x)$", fontsize=32)

    # Set legend ################

    ax.legend(loc='lower right', fontsize=20)

# Save file #################

plt.tight_layout()
plt.savefig("hand_drawn_like_style.png")

# Plot ######################

plt.show()
