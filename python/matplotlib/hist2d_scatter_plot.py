#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See:
# - http://jakevdp.github.io/mpl_tutorial/tutorial_pages/tut3.html

import numpy as np
import matplotlib.pyplot as plt

# MAKE DATA ###################################################################

x, y = np.random.normal(size=(2, 100000))

# INIT FIGURE #################################################################

fig = plt.figure(figsize=(8.0, 8.0))
ax = fig.add_subplot(111)

# AX ##########################################################################

xbins = np.linspace(x.min(), x.max(), 70)
ybins = np.linspace(y.min(), y.max(), 70)

hist, xedges, yedges = np.histogram2d(x, y, bins=(xbins, ybins))

# See http://stackoverflow.com/questions/27156381/python-creating-a-2d-histogram-from-a-numpy-matrix

xidx = np.clip(np.digitize(x, xedges), 0, hist.shape[0]-1)
yidx = np.clip(np.digitize(y, yedges), 0, hist.shape[1]-1)
c = hist[xidx, yidx]

sc = ax.scatter(x, y,
                c=c,
                s=5,
                marker='o',
                #cmap='gnuplot2',
                linewidth=0,
                alpha=1)
fig.colorbar(sc, ax=ax)

# SHOW AND SAVE FILE ##########################################################

plt.tight_layout()

plt.savefig("hist2d_scatter_plot.png")
plt.show()
