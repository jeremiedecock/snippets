#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(6)
y = x
y_err = y / 2.

plt.errorbar(x, y, yerr=y_err, fmt='-o')
plt.show()
