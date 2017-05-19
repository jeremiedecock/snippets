#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make a histogram using a logarithmic scale on X and Y axis

See:

- http://stackoverflow.com/questions/6855710/how-to-have-logarithmic-bins-in-a-python-histogram
"""

import numpy as np
import matplotlib.pyplot as plt

# SETUP #######################################################################

# histtype : [‘bar’ | ‘barstacked’ | ‘step’ | ‘stepfilled’]
HIST_TYPE='bar'
ALPHA=0.5

# MAKE DATA ###################################################################

data = np.random.exponential(size=1000000)
#data = np.abs(np.random.normal(size=1000000) * 10000.)
#data = np.random.chisquare(10, size=1000000)

# INIT FIGURE #################################################################

fig = plt.figure(figsize=(8.0, 6.0))

# AX1 #########################################################################

ax1 = fig.add_subplot(211)

res_tuple = ax1.hist(data,
                     bins=50,
                     histtype=HIST_TYPE,
                     alpha=ALPHA)

ax1.set_title("Normal scale")
ax1.set_xlabel("Value")
ax1.set_ylabel("Count")

# AX2 #########################################################################

ax2 = fig.add_subplot(212)

vmin = np.log10(data.min())
vmax = np.log10(data.max())
bins = np.logspace(vmin, vmax, 50) # <- make a range from 10**vmin to 10**vmax

print(bins)

res_tuple = ax2.hist(data,
                     log=True,                # <- Activate log scale on Y axis
                     bins=bins,
                     histtype=HIST_TYPE,
                     alpha=ALPHA)

ax2.set_xscale("log")              # <- Activate log scale on X axis

ax2.set_title("Log scale")
ax2.set_xlabel("Value")
ax2.set_ylabel("Count")

# SHOW AND SAVE FILE ##########################################################

plt.tight_layout()

plt.savefig("hist_logscale_xy.png")
plt.show()
