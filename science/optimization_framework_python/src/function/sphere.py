# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

__all__ = ['SphereFunction']

import numpy as np
import function

class SphereFunction(function.ObjectiveFunction):

    def __init__(self, ndim=1):
        self.ndim = ndim
        self.domain_min = -1. * np.ones(ndim)
        self.domain_max =  1. * np.ones(ndim)

    def _eval_one_sample(self, x):
        y = np.dot(x,x)
        return y

    def _eval_multiple_samples(self, x):
        y = np.sum(np.power(x, 2.), 1)
        y = y.reshape([-1,1])
        return y

