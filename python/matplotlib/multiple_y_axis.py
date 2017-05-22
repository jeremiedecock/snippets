#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make multiple plots with a sharex X-axis but independent Y axis

See:

- http://matplotlib.org/examples/pylab_examples/multiple_yaxis_with_spines.html
- http://matplotlib.org/examples/subplots_axes_and_figures/fahrenheit_celsius_scales.html
"""

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x1 = 10 * np.random.standard_normal(10000) + 5.
x2 = 12 * np.random.standard_normal(10000)
nbins = 25
 
fig = plt.figure(figsize=(10.,6.))
 
# Plot two distributions on the same plot #####################################

ax = fig.add_subplot(111)
 
val_of_bins_x1, edges_of_bins_x1, patches_x1 = plt.hist(x1, nbins, range=(-50,50), histtype='step')
val_of_bins_x2, edges_of_bins_x2, patches_x2 = plt.hist(x2, nbins, range=(-50,50), histtype='step')
 
# Compute ratio ###############################################################
 
# This put ratio to zero if val_of_bins_x2 is zero
ratio =np.divide(val_of_bins_x1,
                 val_of_bins_x2,
                 where=(val_of_bins_x2 != 0))
 
# Compute error on ration, null if cannot be computed
error= np.divide(val_of_bins_x1 * np.sqrt(val_of_bins_x2) + val_of_bins_x2 * np.sqrt(val_of_bins_x1),
                 val_of_bins_x2 * val_of_bins_x2,
                 where=(val_of_bins_x2 != 0))
 
# Add the ratio on the existing plot
ax2 = ax.twinx()                         # <- !!!

bincenter = 0.5 * (edges_of_bins_x1[1:] + edges_of_bins_x1[:-1])
ax2.errorbar(bincenter, ratio, yerr=error, fmt='.', color='r', lw=2)

ax.set_xlabel("X")
ax.set_ylabel("Count")
ax2.set_ylabel("Ratio")

# Save file ###################################################################

plt.savefig("multiple_y_axis.png")

# Plot ########################################################################

plt.show()
