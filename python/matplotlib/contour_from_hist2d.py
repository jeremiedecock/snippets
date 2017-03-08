#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x1, y1 = np.random.exponential(size=(2, 100000))
x2, y2 = np.random.exponential(size=(2, 100000)) * 10.

xbins = np.logspace(-2, 3, 30)
ybins = np.logspace(-2, 3, 30)

counts1, xedges, yedges = np.histogram2d(x1, y1, bins=(xbins, ybins))
counts2, xedges, yedges = np.histogram2d(x2, y2, bins=(xbins, ybins))

# Plot data #################

fig, ax = plt.subplots()

max_value = max(np.max(counts1), np.max(counts2))

levels = np.array([0.1*max_value, 0.3*max_value, 0.6*max_value])

cs1 = plt.contour(xedges[:-1], yedges[:-1], counts1.T, levels,
                  linewidths=(2, 2, 3), linestyles=('dotted', 'dashed', 'solid'),
                  alpha=0.5, colors='blue', label="TC")
ax.clabel(cs1, inline=False, fontsize=12)

cs2 = plt.contour(xedges[:-1], yedges[:-1], counts2.T, levels,
                  linewidths=(2, 2, 3), linestyles=('dotted', 'dashed', 'solid'),
                  alpha=0.5, colors='red', label="WT")
ax.clabel(cs2, inline=False, fontsize=12)

#ax.set_xlim(1e1, 1e4)
#ax.set_ylim(1e1, 1e4)

ax.set_yscale('log')
ax.set_xscale('log')

# Set title and labels ######

ax.set_title("Contour", fontsize=20)
ax.set_xlabel(r"$X_1$", fontsize=20)
ax.set_ylabel(r"$X_2$", fontsize=20)

# Set legend ################

lines = [ cs1.collections[0], cs2.collections[0]]
labels = ['E1','E2']
ax.legend(lines, labels, prop={'size': 14}, loc='best', fancybox=True, framealpha=0.5)

# Save file #################

plt.savefig("contour_from_hist2d.png")

# Plot ######################

plt.show()
