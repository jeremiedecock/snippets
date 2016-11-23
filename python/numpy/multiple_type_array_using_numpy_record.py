#!/usr/bin/env python

# See http://docs.astropy.org/en/stable/io/fits/usage/table.html#what-is-a-record-array

import numpy as np

foo = np.rec.array([
                    (1, 'Sirius', -1.45, 'A1V'),
                    (2, 'Canopus', -0.73, 'F0Ib'),
                    (3, 'Rigil Kent', -0.1, 'G2V')
                   ],
                   formats='int16, a20, float32, a10',
                   names='order, name, mag, Sp')

print(foo)
print(foo.dtype)
