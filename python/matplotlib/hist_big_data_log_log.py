#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plot a loglog histogram of a large input data (larger than memory), filling the histogram chunk by chunk.

See:
- https://stackoverflow.com/questions/33371917/how-to-plot-result-of-np-histogram-with-matplotlib-analog-to-plt-his
- https://stackoverflow.com/questions/5328556/histogram-matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt

mu, sigma = 1000, 1000

# Build histogram chunk by chunk ######

vmin = -1.
vmax = 4.
nbins = 200

bins = np.logspace(vmin, vmax, nbins)

hist, bins = np.histogram([], bins=bins)
for data in range(100000):
    samples = np.random.normal(loc=mu, scale=sigma, size=100)
    hist += np.histogram(samples, bins=bins)[0]

# Plot data ###########################

fig, ax = plt.subplots(figsize=(10, 10))

ax.step(bins[:-1], hist, linewidth=1.5, label=r'X = $\mathcal{N}(1000, 1000)$')

ax.set_xscale('log')
ax.set_yscale('log')

# Set title and labels ################

ax.set_title("Big data histogram ({} samples)".format(sum(hist)), fontsize=20)
ax.set_xlabel("X", fontsize=32)
ax.set_ylabel("Counts", fontsize=32)

# Set legend ##########################

ax.legend(loc='best', fontsize=16)

# Save file ###########################

plt.savefig("hist_big_data_log_log.png")

# Plot ################################

plt.show()
