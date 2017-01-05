#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This minimal example is taken from
http://www.deeplearning.net/software/theano/introduction.html.
"""

import theano
from theano import tensor

# declare two symbolic floating-point scalars
a = tensor.dscalar()
b = tensor.dscalar()

# create a simple expression
c = a + b

# convert the expression into a callable object that takes (a,b)
# values as input and computes a value for c
f = theano.function([a,b], c)

print(f(1.5, 2.5))

# bind 1.5 to 'a', 2.5 to 'b', and evaluate 'c'
assert 4.0 == f(1.5, 2.5)

