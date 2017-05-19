#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

"""
Set the data limits for the x and y axis
"""

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x = np.arange(-10., 10., 0.1)
y = np.cos(x)

# Plot data #################

fig, ax = plt.subplots(1, 1)

ax.plot(x, y)

ax.set_xlim([-np.pi, np.pi])
ax.set_ylim([-1, 1])

# Save file and plot ########

plt.savefig("ax_set_xylim.png")
plt.show()
