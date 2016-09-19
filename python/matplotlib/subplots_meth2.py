#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-10, 10, 0.1)

fig, axs = plt.subplots(2, 3, figsize=(14, 8))

y1 = np.cos(x)
axs[0][0].plot(x, y1)
axs[0][0].set_title(r"$\cos(x)$")

y2 = np.sin(x)
axs[0][1].plot(x, y2)
axs[0][1].set_title(r"$\sin(x)$")

y3 = np.tan(x)
axs[0][2].plot(x, y3)
axs[0][2].set_title(r"$\tan(x)$")

y4 = np.cosh(x)
axs[1][0].plot(x, y4)
axs[1][0].set_title(r"$\cosh(x)$")

y5 = np.sinh(x)
axs[1][1].plot(x, y5)
axs[1][1].set_title(r"$\sinh(x)$")

y6 = np.tanh(x)
axs[1][2].plot(x, y6)
axs[1][2].set_title(r"$\tanh(x)$")

plt.show()
