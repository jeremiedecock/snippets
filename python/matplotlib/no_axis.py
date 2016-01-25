#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import matplotlib.pyplot as plt

# Plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

x = np.arange(-10., 10., 0.1)

ax1.plot(x, np.cos(x))
ax1.set_title(r"$\cos(x)$")

ax2.plot(x, np.sin(x))
ax2.set_title(r"$\sin(x)$")

ax1.set_axis_off()
ax2.set_axis_off()

plt.show()
