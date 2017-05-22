#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

"""
Make subplots (alternative method 3)
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-10, 10, 0.1)

fig = plt.figure(figsize=(14, 8))

ax1 = plt.subplot(231)
ax2 = plt.subplot(232)
ax3 = plt.subplot(233)
ax4 = plt.subplot(234)
ax5 = plt.subplot(235)
ax6 = plt.subplot(236)

y1 = np.cos(x)
ax1.plot(x, y1)
ax1.set_title(r"$\cos(x)$")

y2 = np.sin(x)
ax2.plot(x, y2)
ax2.set_title(r"$\sin(x)$")

y3 = np.tan(x)
ax3.plot(x, y3)
ax3.set_title(r"$\tan(x)$")

y4 = np.cosh(x)
ax4.plot(x, y4)
ax4.set_title(r"$\cosh(x)$")

y5 = np.sinh(x)
ax5.plot(x, y5)
ax5.set_title(r"$\sinh(x)$")

y6 = np.tanh(x)
ax6.plot(x, y6)
ax6.set_title(r"$\tanh(x)$")

plt.show()
