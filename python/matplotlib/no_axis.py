#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

"""
Don't show axis
"""

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x = np.arange(-10., 10., 0.1)
y1 = np.cos(x)
y2 = np.sin(x)

# Plot data #################

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

ax1.plot(x, y1)
ax1.set_title(r"$\cos(x)$")

ax2.plot(x, y2)
ax2.set_title(r"$\sin(x)$")

ax1.set_axis_off()
ax2.set_axis_off()

# Save file and plot ########

plt.savefig("no_axis.png")
plt.show()
