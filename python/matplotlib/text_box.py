#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016,2017 Jérémie DECOCK (http://www.jdhp.org)

"""
Add a text box
"""

import matplotlib.pyplot as plt
import numpy as np

fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

data = np.random.binomial(n=100, p=0.25, size=10000)
ax1.hist(data)

# Info box
ax1.text(0.05, 0.92,
         "Hello world!\nThis is a text box demo",
         verticalalignment = 'top',
         horizontalalignment = 'left',
         transform = ax1.transAxes,
         bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})

# Info box
ax1.text(0.95, 0.92,
         "Another text box",
         verticalalignment = 'top',
         horizontalalignment = 'right',
         transform = ax1.transAxes,
         bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})

# Save file and plot ########

plt.savefig("text_box.png", bbox_inches='tight')
plt.show()
