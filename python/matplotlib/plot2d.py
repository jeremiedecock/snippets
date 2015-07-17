#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt

def main():
    x_vec = np.arange(-10, 10, 0.01)
    y_vec = np.sin(2 * 2 * np.pi * x_vec) * 1/np.sqrt(2*np.pi) * np.exp(-(x_vec**2)/2)

    fig = plt.figure(figsize=(16.0, 10.0))
    ax = fig.add_subplot(111)
    ax.plot(x_vec, y_vec, "-", label="Test")

    # TITLE AND LABELS
    ax.set_title(r"Test", fontsize=20)
    ax.set_xlabel(r"$x$", fontsize=32)
    ax.set_ylabel(r"$f(x)$", fontsize=32)

    # LEGEND
    ax.legend(loc='lower right', fontsize=20)

    # SAVE FILES ######################
    plt.savefig("plot2d.png")

    # PLOT ############################
    plt.show()

if __name__ == "__main__":
    main()

