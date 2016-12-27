#!/usr/bin/env python

# See https://docs.scipy.org/doc/numpy/user/basics.rec.html
#     http://stackoverflow.com/questions/16621351/how-to-use-python-numpy-savetxt-to-write-strings-and-float-number-to-an-ascii-fi

import numpy as np

# METH 1

foo = np.array([
                   (1, 'Sirius', -1.45, 'A1V'),
                   (2, 'Canopus', -0.73, 'F0Ib'),
                   (3, 'Rigil Kent', -0.1, 'G2V')
               ],
               dtype='int16, a20, float32, a10')

print(foo)
print(foo.dtype)

# METH 2

foo = np.array([
                   (1, 'Sirius', -1.45, 'A1V'),
                   (2, 'Canopus', -0.73, 'F0Ib'),
                   (3, 'Rigil Kent', -0.1, 'G2V')
               ],
               dtype=[
                   ('order', 'int16'),
                   ('name', 'a20'),
                   ('mag', 'float32'),
                   ('Sp', 'a10')
               ])

print(foo)
print(foo.dtype)

# METH 3

foo = np.array([
                   (1, 'Sirius', -1.45, 'A1V'),
                   (2, 'Canopus', -0.73, 'F0Ib'),
                   (3, 'Rigil Kent', -0.1, 'G2V')
               ],
               dtype={
                   'names': ['order', 'name', 'mag', 'Sp'],
                   'formats': ['int16', 'a20', 'float32', 'a10']
               })

print(foo)
print(foo.dtype)
