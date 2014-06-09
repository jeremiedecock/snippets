#!/usr/bin/env python
# -*- coding: utf-8 -*-
            
# see http://stackoverflow.com/questions/11373192/generating-discrete-random-variables-with-specified-weights-using-scipy-or-numpy

import numpy as np
from scipy.stats import rv_discrete  


# IF VALUES ARE INTEGERS ########################

values = [1, 2, 3]
probabilities = [0.2, 0.5, 0.3]
num_samples = 1000

# A Scipy probability distribution
distrib = rv_discrete(values=(values, probabilities))

# One sample
value = distrib.rvs()
print "value =", value

# Multiple samples
values = distrib.rvs(size=num_samples)

print values

print "Percentage of 1:", float(values.tolist().count(1)) / num_samples 
print "Percentage of 2:", float(values.tolist().count(2)) / num_samples
print "Percentage of 3:", float(values.tolist().count(3)) / num_samples



# IF VALUES ARE FLOATS ##########################

print

values = np.array([1.1, 2.2, 3.3])
probabilities = [0.2, 0.5, 0.3]

# A Scipy probability distribution (values have to be integers)
distrib = rv_discrete(values=(range(len(values)), probabilities))

# Samples
indexes = distrib.rvs(size=100)

print indexes
print values[indexes]
