# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

__all__ = ['Sin3Function']

import numpy as np
import function

class Sin3Function(function.ObjectiveFunction):

    def __init__(self):
        self.ndim = 2
        self.domain_min = -10. * np.ones(self.ndim)
        self.domain_max =  10. * np.ones(self.ndim)

    def _eval_one_sample(self, x):
        r = np.sqrt(np.power(x[0], 2) + np.power(x[1], 2))
        y = np.sin(r)
        return y

    def _eval_multiple_samples(self, x):
        r = np.sqrt(np.power(x[:,0], 2) + np.power(x[:,1], 2))
        y = np.sin(r)
        y = y.reshape([-1,1])
        return y

