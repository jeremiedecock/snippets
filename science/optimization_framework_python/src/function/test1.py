# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import function

class TestFunction1(function.ObjectiveFunction):

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

