#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt

def main():

    x = np.arange(0, 10, 0.05)
    y1 = np.cos(x)
    y2 = np.sin(x)

    plt.plot(x, y1, x, y2)
    plt.fill_between(x, y1, y2, facecolor='red', alpha=0.5)

    # SAVE FILES ######################
    plt.savefig("fill.png")

    plt.show()

if __name__ == "__main__":
    main()

