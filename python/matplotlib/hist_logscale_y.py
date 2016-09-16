#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See:
# - 

import numpy as np
import matplotlib.pyplot as plt

# SETUP #######################################################################

# histtype : [‘bar’ | ‘barstacked’ | ‘step’ | ‘stepfilled’]
HIST_TYPE='bar'
ALPHA=0.5

# MAKE DATA ###################################################################

gaussian_numbers_array = np.random.normal(size=1000000)

# INIT FIGURE #################################################################

fig = plt.figure(figsize=(8.0, 6.0))

# AX1 #########################################################################

ax1 = fig.add_subplot(211)

res_tuple = ax1.hist(gaussian_numbers_array,
                     bins=50,
                     histtype=HIST_TYPE,
                     alpha=ALPHA)

ax1.set_title("Normal scale")
ax1.set_xlabel("Value")
ax1.set_ylabel("Count")

# AX2 #########################################################################

ax2 = fig.add_subplot(212)

res_tuple = ax2.hist(gaussian_numbers_array,
                     log=True,                # <- Activate log scale on Y axis
                     bins=50,
                     histtype=HIST_TYPE,
                     alpha=ALPHA)

ax2.set_title("Log scale")
ax2.set_xlabel("Value")
ax2.set_ylabel("Count")

# SHOW AND SAVE FILE ##########################################################

plt.tight_layout()

plt.savefig("hist_logscale_y.png")
plt.show()
