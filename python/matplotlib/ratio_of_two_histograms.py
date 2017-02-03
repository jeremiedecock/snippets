#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: http://matplotlib.org/examples/pylab_examples/multiple_yaxis_with_spines.html
#      http://matplotlib.org/examples/subplots_axes_and_figures/fahrenheit_celsius_scales.html

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x1 = np.random.normal(loc=5.0, scale=10.0, size=10000)
x2 = np.random.normal(loc=0.0, scale=12.0, size=10000)

nbins = 25
 
fig = plt.figure(figsize=(10.,6.))
 
# Plot two distributions on the same plot #####################################

ax1 = fig.add_subplot(121)
ax1.set_ylabel('counts')
 
val_of_bins_x1, edges_of_bins_x1, patches_x1 = plt.hist(x1, nbins, range=(-50,50), histtype='step', label="x1")
val_of_bins_x2, edges_of_bins_x2, patches_x2 = plt.hist(x2, nbins, range=(-50,50), histtype='step', label="x2")
 
print("bins:", edges_of_bins_x1)

# Compute ratio ###############################################################
 
# Set ratio where val_of_bins_x2 is not zero

ratio = np.divide(val_of_bins_x1,
                  val_of_bins_x2,
                  where=(val_of_bins_x2 != 0))

print("ratio:", ratio)
 
# Compute error on ratio (null if cannot be computed)

error = np.divide(val_of_bins_x1 * np.sqrt(val_of_bins_x2) + val_of_bins_x2 * np.sqrt(val_of_bins_x1),
                  np.power(val_of_bins_x2, 2),
                  where=(val_of_bins_x2 != 0))

print("error:", error)
 
# Add the ratio on the existing plot

ax2 = ax1.twinx()
ax2.set_ylabel('ratio')

bincenter = 0.5 * (edges_of_bins_x1[1:] + edges_of_bins_x1[:-1])
plt.errorbar(bincenter, ratio, yerr=error, fmt='.', color='r')
 
# Add an histogram of errors

ax3 = fig.add_subplot(122)
ax3.set_xlabel('error')
ax3.set_ylabel('count')

plt.hist(error, nbins)

# Save file ###################################################################

fig.tight_layout()

plt.savefig("ratio_of_two_histograms.png")

# Plot ########################################################################

plt.show()
