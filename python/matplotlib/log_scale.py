#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use a logarithmic scale on both axis
"""

import math
import numpy as np
import matplotlib.pyplot as plt

# Build datas ###############

#x = np.arange(0.1, 100, 1)  # bad
x = np.exp(np.arange(0, 3, 0.05) * math.log(10))

print(x)

yl1 = np.log(x)
yl2 = x * np.log(x)
y1 = x
y2 = np.power(x,2)
y3 = np.power(x,3)
ye = np.exp(x * math.log(2))

# Plot data #################

plt.plot(x, yl1, ".", x, yl2, ".", x, y1, ".", x, y2, ".", x, y3, ".", ye, "--")
plt.xscale('log')
plt.yscale('log')

plt.xlabel(r'$x$')
plt.ylabel(r'$f(y)$')

plt.legend(["log(x)", "x log(x)", "x", "x^2", "x^3", "2^x"])

plt.title('log scale')

plt.ylim(ymax = math.exp(20 * math.log(10)))

# Save file and plot ########

plt.savefig("log_scale.png")
plt.show()
