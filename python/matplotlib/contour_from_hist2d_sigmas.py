#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x, y = np.random.normal(size=(2, 1000000))

xbins = np.linspace(-2, 2, 30)
ybins = np.linspace(-2, 2, 30)

counts, xedges, yedges = np.histogram2d(x, y, bins=(xbins, ybins))

print("std(x)=", np.std(x))
print("std(y)=", np.std(y))

# Plot data #################

fig, ax = plt.subplots()

sigmas = [1., 2., 3.]
levels = []
fmt = {}

for sigma in sigmas:
    levels.append(float(sigma) * np.std(counts))
    fmt[float(sigma) * np.std(counts)] = r"${}\sigma$".format(int(sigma))

cs = plt.contour(xedges[:-1], yedges[:-1], counts.T, levels,
                  linewidths=(2, 2, 3), linestyles=('dotted', 'dashed', 'solid'),
                  alpha=0.8, colors='red')
ax.clabel(cs, inline=True, fontsize=16, fmt=fmt)

# Set title and labels ######

ax.set_title("Contour", fontsize=20)
ax.set_xlabel(r"$X_1$", fontsize=20)
ax.set_ylabel(r"$X_2$", fontsize=20)

# Set legend ################

lines = [ cs.collections[0]]
labels = [r'$\mathcal{N}$']
ax.legend(lines, labels, prop={'size': 14}, loc='best', fancybox=True, framealpha=0.5)

# Save file #################

plt.savefig("contour_from_hist2d_sigmas.png")

# Plot ######################

plt.show()
