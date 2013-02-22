#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np


# OPTIMIZERS ##################################################################

class NaiveMinimizer:
    
    def optimize(self, objective_function, num_samples=100):

        x = np.random.random([num_samples, objective_function.ndim])
        y = objective_function(x)
        x_min = x[np.argmin(y), :]

        print np.shape(x), np.shape(y)
        print x
        print y
        print np.min(y)
        print np.argmin(y)
        print x[np.argmin(y), :]

        return x_min


class SAES:

    def optimize(self):

        best_x = np.random()
        for i in range(100):
            x = np.random()
            y = objective_function(x)
            print x, y
        return best_x

