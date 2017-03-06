#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See:
# - http://jakevdp.github.io/mpl_tutorial/tutorial_pages/tut3.html

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# MAKE DATA ###################################################################

x, y = np.random.exponential(size=(2, 100000))

# INIT FIGURE #################################################################

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

# AX1 #########################################################################

xbins = np.linspace(x.min(), x.max(), 70)
ybins = np.linspace(y.min(), y.max(), 70)

hist, xedges, yedges = np.histogram2d(x, y, bins=(xbins, ybins))

# See http://stackoverflow.com/questions/27156381/python-creating-a-2d-histogram-from-a-numpy-matrix

xidx = np.clip(np.digitize(x, xedges), 0, hist.shape[0]-1)
yidx = np.clip(np.digitize(y, yedges), 0, hist.shape[1]-1)
c = hist[xidx, yidx]

sc = ax1.scatter(x, y,
                 c=c,
                 s=5,
                 marker='o',
                 #cmap='gnuplot2',
                 linewidth=0,
                 alpha=1)
fig.colorbar(sc, ax=ax1)

ax1.set_xlim(xmin=0)
ax1.set_ylim(ymin=0)

ax1.set_title("Normal scale")

# AX2 #########################################################################

x = np.log10(x)
y = np.log10(y)

xbins = np.linspace(x.min(), x.max(), 70)
ybins = np.linspace(y.min(), y.max(), 70)

hist, xedges, yedges = np.histogram2d(x, y, bins=(xbins, ybins))

# See http://stackoverflow.com/questions/27156381/python-creating-a-2d-histogram-from-a-numpy-matrix

xidx = np.clip(np.digitize(x, xedges), 0, hist.shape[0]-1)
yidx = np.clip(np.digitize(y, yedges), 0, hist.shape[1]-1)
c = hist[xidx, yidx]

sc = ax2.scatter(x, y,
                 c=c,
                 s=5,
                 marker='o',
                 #cmap='gnuplot2',
                 linewidth=0,
                 alpha=1)
fig.colorbar(sc, ax=ax2)

# Use "10^n" instead "n" as ticks label
func_formatter = lambda x, pos: r'$10^{{{}}}$'.format(int(x))
ax2.xaxis.set_major_formatter(FuncFormatter(func_formatter))
ax2.yaxis.set_major_formatter(FuncFormatter(func_formatter))

ax2.set_title("Log scale")

# SHOW AND SAVE FILE ##########################################################

plt.tight_layout()

plt.savefig("hist2d_scatter_plot_logscale_xy.png")
plt.show()
