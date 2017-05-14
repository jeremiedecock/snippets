#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

import matplotlib.patches as patches
import matplotlib.lines as mlines

# Plot data #################

fig, ax = plt.subplots(figsize=(5, 5))
ax.axis('equal')
plt.axis([-10, 10, -10, 10])

line = mlines.Line2D((-7, 7), (-7, 7), lw=2, color="g")
line.set_zorder(1)     # <- PUT THE LINE BELOW THE CIRCLE
ax.add_line(line)

circle = patches.Circle((0, 0), 3, fill=True, edgecolor="b", facecolor="r")
circle.set_zorder(2)   # <- PUT THE CIRCLE ON TOP
ax.add_patch(circle)

# Save file #################

plt.savefig("zorder.png")

# Plot ######################

plt.show()
