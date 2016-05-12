#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x = np.arange(-10., 10., 0.1)
y = np.power(x, 2)

# Plot data #################

fig, ax = plt.subplots(1, 1)

ax.plot(x, y)

ax.set_title(r"$x^2$")

# Save file and plot ########

plt.savefig("ax_set_title.png")
plt.show()
