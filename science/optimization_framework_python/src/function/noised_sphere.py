# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import function

# STOCHASTIC OBJECTIVE FUNCTIONS ##############################################

class NoisedSphereFunction(function.ObjectiveFunction):

    def __init__(self, ndim=1, sigma=0.1):
        self.ndim = ndim
        self.domain_min = -1. * np.ones(ndim)
        self.domain_max =  1. * np.ones(ndim)

        self.sigma = sigma

    def __call__(self, *pargs, **kargs):
        x = pargs[0]

        if x.ndim == 1:
            # Only one sample
            y = np.sum(np.power(x, 2.))
            y = y + np.random.normal(0., self.sigma)
        else:
            # Multiple samples
            y = np.sum(np.power(x, 2.), 1)
            y = y + np.random.normal(0., self.sigma, y.shape[0])
            y = y.reshape([-1,1])

        return y

