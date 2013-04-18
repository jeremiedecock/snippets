# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

__all__ = ['NoisedSphereFunction']

import numpy as np
import function

# STOCHASTIC OBJECTIVE FUNCTIONS ##############################################

# TODO: this class should be generic: take an other class as argument
#       of the constructor and simply add noise on the evaluations of
#       it.

class NoisedSphereFunction(function.ObjectiveFunction):

    def __init__(self, ndim=1, sigma=0.1):
        self.ndim = ndim
        self.domain_min = -1. * np.ones(ndim)
        self.domain_max =  1. * np.ones(ndim)

        self.sigma = sigma

    def _eval_one_sample(self, x):
        y = np.dot(x,x)
        y = y + np.random.normal(0., self.sigma)
        return y

    def _eval_multiple_samples(self, x):
        y = np.sum(np.power(x, 2.), 1)
        y = y + np.random.normal(0., self.sigma, y.shape[0])
        y = y.reshape([-1,1])
        return y

