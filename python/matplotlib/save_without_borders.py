#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Remove borders on saved figures
"""

import matplotlib.pyplot as plt
import numpy as np

fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))

x = np.arange(-10, 10, 0.1)
y = np.power(x, 2.)

ax1.plot(x, y)

# Save file and plot ########

output_file = "save_without_borders.png"

plt.savefig(output_file, bbox_inches='tight')
plt.show()
