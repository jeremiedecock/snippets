#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np


class ObjectiveFunction:
    pass

# TODO: doit être un objet qui permet de connaître:
# - le dommaine de définition de x
#   - continu / discret ?
#   - contraint ou non
# - le nombre de dimensions de x

# OBJECTIVE FUNCTIONS #########################################################

class SphereFunction(ObjectiveFunction):

    def __init__(self, ndim=1):
        self.ndim = ndim
        self.domain_min = -1. * np.ones(ndim)
        self.domain_max =  1. * np.ones(ndim)

    def __call__(self, *pargs, **kargs):
        x = pargs[0]

        if x.ndim == 1:
            # Only one sample
            y = np.sum(np.power(x, 2.))
        else:
            # Multiple samples
            y = np.sum(np.power(x, 2.), 1).reshape([-1,1])

        return y


class TestFunction1(ObjectiveFunction):

    def __init__(self):
        self.ndim = 2
        self.domain_min = -10. * np.ones(self.ndim)
        self.domain_max =  10. * np.ones(self.ndim)

    def __call__(self, *pargs, **kargs):
        x = pargs[0]

        if x.ndim == 1:
            # Only one sample
            r = np.sqrt(np.power(x[0], 2) + np.power(x[1], 2))
            y = np.sin(r)
        else:
            # Multiple samples
            r = np.sqrt(np.power(x[:,0], 2) + np.power(x[:,1], 2))
            y = np.sin(r).reshape([-1,1])

        return y

# STOCHASTIC OBJECTIVE FUNCTIONS ##############################################

class NoisedSphereFunction(ObjectiveFunction):

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


