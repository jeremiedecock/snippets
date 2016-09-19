#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x = np.arange(6)
y = x
y_err = y / 2.

# Plot data #################

plt.errorbar(x, y, yerr=y_err, fmt='-o')

# Save file and plot ########

plt.savefig("error_bar.png")
plt.show()
