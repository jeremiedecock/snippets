#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Realtime animation

See http://stackoverflow.com/questions/11874767/real-time-plotting-in-while-loop-with-matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt

import random
import time

X_DELTA = 1
TIME_SLEEP = 0.1
MAX_VALUES = 15
Y_MIN = 0
Y_MAX = 1

def main():

    plt.ion()    # setup interactive mode
    plt.show()

    x_vec = []
    y_vec = []

    x_value = 0

    while True:
        x_vec.append(x_value)
        y_vec.append(random.random())

        if len(x_vec) > MAX_VALUES:
            x_vec.pop(0)
            y_vec.pop(0)

        plt.clf()

        plt.xlim(x_vec[0], x_vec[-1])
        plt.ylim(Y_MIN, Y_MAX)

        plt.plot(x_vec, y_vec, "-")
        plt.draw()

        time.sleep(TIME_SLEEP)

        x_value += X_DELTA

if __name__ == "__main__":
    main()

