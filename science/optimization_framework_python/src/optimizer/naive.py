# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

__all__ = ['NaiveMinimizer']

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import warnings

import optimizer

class NaiveMinimizer(optimizer.Optimizer):
    
    def optimize(self, objective_function, num_samples=1000):

        dmin = objective_function.domain_min
        dmax = objective_function.domain_max
        
        x_samples = np.random.uniform(dmin, dmax, [num_samples, objective_function.ndim])
        y_samples = objective_function(x_samples)
        x_min = x_samples[y_samples.argmin(), :]

        self.plotSamples(x_samples, y_samples)
        self.plotCosts(y_samples)

        return x_min

