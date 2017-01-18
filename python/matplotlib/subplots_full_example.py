#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Jérémie DECOCK (http://www.jdhp.org)

import math
from matplotlib import pyplot as plt
import numpy as np

def plot(axis,
         data_list,
         bins_min,
         bins_max,
         label_list,
         title=None,
         logx=False,
         logy=False,
         hist_type="bar",
         alpha=0.5,
         linear_xlabel_style='sci',
         linear_ylabel_style='sci',
         num_bins=None):

    if logx:
        # Setup the logarithmic scale on the X axis
        vmin = np.log10(bins_min)
        vmax = np.log10(bins_max)

        # Make a range from 10**vmin to 10**vmax
        bins = np.logspace(vmin, vmax, num_bins if num_bins is not None else 50)
    elif num_bins is not None:
        bins = np.linspace(bins_min, bins_max, num_bins)
    else:
        bins = range(math.floor(bins_min), math.ceil(bins_max))

    axis.hist(data_list,
              bins=bins,
              log=logy,                      # Set log scale on the Y axis
              histtype=hist_type,
              alpha=alpha,
              label=label_list)

    axis.legend(prop={"size": 20})

    axis.set_ylabel("Count", fontsize=16)
    axis.set_xlabel(r"$x$", fontsize=16)

    if title is not None:
        axis.set_title(title, fontsize=20)

    plt.setp(axis.get_xticklabels(), fontsize=14)
    plt.setp(axis.get_yticklabels(), fontsize=14)

    if logx:
        axis.set_xscale("log")               # Activate log scale on X axis
    elif linear_xlabel_style == 'sci':
        axis.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    
    if (not logy) and (linear_ylabel_style == 'sci'):
        axis.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    axis.set_xlim(xmin=1)

#############################

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(16, 9))

data_list = [np.random.binomial(n=100, p=0.25, size=10000),
             np.random.binomial(n=100, p=0.5,  size=10000)]
label_list = [r"$\mathcal{B}(100, 0.25)$",
              r"$\mathcal{B}(100, 0.5)$"]

plot(ax1, data_list, bins_min=1, bins_max=100, label_list=label_list, title="Linear scale")
plot(ax2, data_list, bins_min=1, bins_max=300, label_list=label_list, title="Log scale on x axis", logx=True)
plot(ax3, data_list, bins_min=1, bins_max=100, label_list=label_list, title="Log scale on y axis", logy=True)
plot(ax4, data_list, bins_min=1, bins_max=300, label_list=label_list, title="Log scale on x and y axis", logx=True, logy=True)

# General title #############

plt.suptitle("Binomial distribution", fontsize=22)

plt.tight_layout()

# http://stackoverflow.com/questions/8248467/matplotlib-tight-layout-doesnt-take-into-account-figure-suptitle
plt.subplots_adjust(top=0.9)

# Save file and plot ########

plt.savefig("subplots_full_example.png", bbox_inches='tight')

plt.show()

