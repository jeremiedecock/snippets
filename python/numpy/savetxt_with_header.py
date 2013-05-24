#!/usr/bin/env python

import numpy as np

a = np.random.rand(10, 4)

fd = open("test.dat", "w")
fd.write("# This is a test\n")
fd.write("# with a header\n")
np.savetxt(fd, a)
fd.close()

