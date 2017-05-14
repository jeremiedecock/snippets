#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

import matplotlib.patches as patches

# Plot data #################

#fig, ax = plt.subplots(figsize=(5, 5))
fig, (ax1, ax2) = plt.subplots(ncols=2)

ax1.plot([0, 1])
ax2.plot([0, 1])

ax2.axis('equal')              # <- SAME SCALE ON X AND Y

# Save file #################

plt.savefig("axis_equal.png")

# Plot ######################

plt.show()
