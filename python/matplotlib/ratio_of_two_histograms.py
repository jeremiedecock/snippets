#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: http://matplotlib.org/examples/pylab_examples/multiple_yaxis_with_spines.html
#      http://matplotlib.org/examples/subplots_axes_and_figures/fahrenheit_celsius_scales.html

import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

x1 = 10 * np.random.standard_normal(10000) + 5.
x2 = 12 * np.random.standard_normal(10000)
nbins = 25
 
fig = plt.figure(figsize=(10.,6.))
 
# Plot two distributions on the same plot #####################################

a1 = fig.add_subplot(121)
 
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
a2 = a1.twinx()

bincenter = 0.5 * (edges_of_bins_x1[1:] + edges_of_bins_x1[:-1])
plt.errorbar(bincenter, ratio, yerr=error, fmt='.', color='r')
 
a3 = fig.add_subplot(122)

plt.hist(error, nbins)

# Save file ###################################################################

plt.savefig("ratio_of_two_histograms.png")

# Plot ########################################################################

plt.show()
