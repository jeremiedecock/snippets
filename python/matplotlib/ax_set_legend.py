#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x = np.arange(-10, 10, 0.01)
y = np.sin(x)

# Plot data #################

fig = plt.figure(figsize=(8.0, 8.0))
ax = fig.add_subplot(111)

ax.plot(x, y, label="Test")

# Set legend ################

ax.legend(loc='lower right', fontsize=20)

# Save file and plot ########

plt.savefig("plot2d.png")
plt.show()
