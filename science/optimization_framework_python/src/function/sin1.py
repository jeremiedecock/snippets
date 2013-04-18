# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

__all__ = ['Sin1Function']

import numpy as np
import function

class Sin1Function(function.ObjectiveFunction):

    def __init__(self):
        self.ndim = 1
        self.domain_min = -10. * np.ones(self.ndim)
        self.domain_max =  10. * np.ones(self.ndim)

    def _eval_one_sample(self, x):
        y = np.sin(2 * 2 * np.pi * x) * 1/np.sqrt(2*np.pi) * np.exp(-(x**2)/2)
        return y

