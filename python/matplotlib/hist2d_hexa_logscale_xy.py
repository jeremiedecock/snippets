#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# MAKE DATA ###################################################################

x, y = np.random.exponential(size=(2, 100000))

# INIT FIGURE #################################################################

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

# AX1 #########################################################################

im = ax1.hexbin(x, y, gridsize=40)
fig.colorbar(im, ax=ax1)

ax1.set_title("Normal scale")

# AX2 #########################################################################

x = np.log10(x)
y = np.log10(y)

im = ax2.hexbin(x, y, gridsize=40)
fig.colorbar(im, ax=ax2)

# Use "10^n" instead "n" as ticks label
func_formatter = lambda x, pos: r'$10^{{{}}}$'.format(int(x))
ax2.xaxis.set_major_formatter(FuncFormatter(func_formatter))
ax2.yaxis.set_major_formatter(FuncFormatter(func_formatter))

ax2.set_title("Log scale")

# SHOW AND SAVE FILE ##########################################################

plt.tight_layout()

plt.savefig("hist2d_hexa_logscale_xy.png")
plt.show()
