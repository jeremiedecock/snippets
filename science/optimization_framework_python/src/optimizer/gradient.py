# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

__all__ = ['GradientDescent']

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import warnings

import optimizer

class GradientDescent(optimizer.Optimizer):

    def __init__(self, delta):
        self.delta = delta

    def optimize(self, objective_function, num_samples=1000):

        dmin = objective_function.domain_min
        dmax = objective_function.domain_max
        
        x = np.random.uniform(dmin, dmax, objective_function.ndim)

        x_samples = np.zeros([num_samples, objective_function.ndim])

        # Compute the gradient of objective_function at x
        for sample_index in range(num_samples):
            nabla = np.zeros(objective_function.ndim)
            for dim_index in range(objective_function.ndim):
                delta_vec = np.zeros(objective_function.ndim)
                delta_vec[dim_index] = self.delta

                y1 = objective_function(x - delta_vec)
                y2 = objective_function(x + delta_vec)

                nabla[dim_index] = y2 - y1

            x = x - nabla

            # Keep an history of x to plot things...
            x_samples[sample_index, :] = x

        y_samples = objective_function(x_samples)
        self.plotSamples(x_samples, y_samples)
        self.plotCosts(y_samples)

        return x

