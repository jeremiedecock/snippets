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

ax.plot(x, y)

# Set labels ################

ax.set_xlabel(r"$x$", fontsize=32)
ax.set_ylabel(r"$f(x)$", fontsize=32)

# Save file and plot ########

plt.savefig("ax_set_label.png")
plt.show()
