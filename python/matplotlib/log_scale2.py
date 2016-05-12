#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x = np.arange(1000)
y = x * x

# Plot data #################

plt.plot(x, y)
plt.yscale('log')

plt.title(r'$x^2$')

# Save file and plot ########

plt.savefig("log_scale2.png")
plt.show()
