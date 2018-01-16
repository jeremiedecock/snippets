#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plot an histogram with a text stats summary

See:

- https://stackoverflow.com/questions/8482588/putting-text-in-top-left-corner-of-matplotlib-plot
"""

import numpy as np
import matplotlib.pyplot as plt

# MAKE DATA ###################################################################

data = np.random.normal(size=1000)

# AX1 #########################################################################

fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(7, 7))
    
ax.hist(data,
         bins=50,
         #range=(-10, 2500),
         log=False)

ax.set_ylabel("Counts", fontsize=18)
ax.set_title("Gaussian", fontsize=20)
    
sig_info = "Samples: {}\nMin: {:0.2f}\nMax: {:0.2f}\nMean: {:0.2f}\nSTD: {:0.2f}".format(len(data),
                                                                                         data.min(),
                                                                                         data.max(),
                                                                                         data.mean(),
                                                                                         data.std())

ax.text(0.95, 0.95, sig_info,
         horizontalalignment='right',
         verticalalignment='top',
         fontsize=18,
         transform = ax.transAxes)
print(sig_info)

# SHOW AND SAVE FILE ##########################################################

plt.tight_layout()

plt.savefig("text_box.png")
plt.show()
