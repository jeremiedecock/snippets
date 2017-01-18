#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016,2017 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

data = np.random.binomial(n=100, p=0.25, size=10000)
ax1.hist(data)

# See http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.tick_params
ax1.tick_params(axis='both',       # changes apply to the x and y axis
                which='both',      # both major and minor ticks are affected
                bottom='on',       # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                left='on',         # ticks along the left edge are off
                right='off',       # ticks along the right edge are off
                labelbottom='off', # labels along the bottom edge are off
                labelleft='off')   # labels along the lefleft are off

# Save file and plot ########

plt.savefig("no_ticks_and_labels.png", bbox_inches='tight')
plt.show()
