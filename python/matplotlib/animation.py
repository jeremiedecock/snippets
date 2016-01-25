#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

import math
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

# Plots
fig, ax = plt.subplots()

def update(frame):
    x = np.arange(frame/10., frame/10. + 2. * math.pi, 0.1)
    ax.clear()
    ax.plot(x, np.cos(x))

    # Optional: save plots
    filename = "img_{:03}.png".format(frame)
    plt.savefig(filename)

# Note: "interval" is in ms
anim = FuncAnimation(fig, update, interval=100)

plt.show()
