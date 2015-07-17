#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(1000)
y = x * x

plt.plot(x, y)
plt.yscale('log')

plt.title('x^2')

# SAVE FILES ######################
plt.savefig("log_scale2.png")

plt.show()
