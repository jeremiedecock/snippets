# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np

class State:

    #self.ndim
    #self.position
    #self.velocity

    def __init__(self, ndim):
        self.ndim = ndim
        self.position = np.zeros(self.ndim)
        self.velocity = np.zeros(self.ndim)


#    def __init__(self, initial_position=None, initial_velocity=None):
#
#        if (initial_position is not None) and (initial_position is not None):
#            # TODO: additional checks -> np.array, same shape, ndim=1
#            self.ndim = initial_position.shape[0]
#            self.position = initial_position
#            self.velocity = initial_velocity
#        else:
#            self.ndim = 1
#            self.position = np.zeros(self.ndim)
#            self.velocity = np.zeros(self.ndim)


#    def __str__(self):
#        pass


