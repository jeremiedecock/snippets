#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Jérémie DECOCK (http://www.jdhp.org)

from matplotlib import pyplot as plt
import numpy as np

def plot(axis, data, bins, label_list, title, logx=False, logy=False):
    axis.hist(data,
              bins,
              log=logy,
              histtype="bar",
              alpha=0.5,
              label=label_list)

    axis.legend(prop={"size": 20})

    axis.set_ylabel("Count", fontsize=16)
    axis.set_xlabel(r"$x$", fontsize=16)

    axis.set_title(title, fontsize=20)

    plt.setp(axis.get_xticklabels(), fontsize=14)
    plt.setp(axis.get_yticklabels(), fontsize=14)

    if logx:
        axis.set_xscale("log")               # Activate log scale on X axis
    else:
        axis.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    
    if not logy:
        axis.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    axis.set_xlim(xmin=1)

#############################

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(16, 9))

data = [np.random.binomial(n=100, p=0.25, size=10000),
        np.random.binomial(n=100, p=0.5,  size=10000)]
label_list = [r"$\mathcal{B}(100, 0.25)$",
              r"$\mathcal{B}(100, 0.5)$"]
bins = range(300)

plot(ax1, data, bins=bins, label_list=label_list, title="Linear scale")
plot(ax2, data, bins=bins, label_list=label_list, title="Log scale on x axis", logx=True)
plot(ax3, data, bins=bins, label_list=label_list, title="Log scale on y axis", logy=True)
plot(ax4, data, bins=bins, label_list=label_list, title="Log scale on x and y axis", logx=True, logy=True)

# General title #############

plt.suptitle("Binomial distribution", fontsize=22)

plt.tight_layout()

# http://stackoverflow.com/questions/8248467/matplotlib-tight-layout-doesnt-take-into-account-figure-suptitle
plt.subplots_adjust(top=0.9)

# Save file and plot ########

plt.savefig("subplots_full_example.png", bbox_inches='tight')

plt.show()

