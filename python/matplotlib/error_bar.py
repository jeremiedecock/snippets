#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(6)
y = x
y_err = y / 2.

plt.errorbar(x, y, yerr=y_err, fmt='-o')

# SAVE FILES ######################
plt.savefig("error_bar.png")

plt.show()
