#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

t = np.linspace(0, np.pi, 100)

x = 0.7 * np.sin(t / 2.) * np.sin(3. / 2. * t)
y = 0.7 * np.cos(t) * np.sin(2. * t)

# Plot data #################

fig = plt.figure(figsize=(8.0, 8.0))
ax = fig.add_subplot(111)

ax.plot(x, y)

# Save file and plot ########

plt.savefig("parametric_curve.png")

plt.show()

