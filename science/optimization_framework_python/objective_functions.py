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

    def __call__(self, *pargs, **kargs):
        x = pargs[0]
        y = np.sum(np.power(x, 2.), 1).reshape([-1,1])
        print "evaluate", x, "=", y
        print
        return y

