# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

__all__ = ['Sin2Function']

import numpy as np
import function

class Sin2Function(function.ObjectiveFunction):

    def __init__(self):
        self.ndim = 1
        self.domain_min = 0. * np.ones(self.ndim)
        self.domain_max = 10. * np.ones(self.ndim)

    def _eval_one_sample(self, x):
        x = np.absolute(x)
        y = np.sin(2 * 2 * np.pi * x) * np.exp(-5 * x)
        return y

