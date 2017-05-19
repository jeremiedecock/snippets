#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make a histogram with weighted values

See:

- http://bespokeblog.wordpress.com/2011/07/11/basic-data-plotting-with-matplotlib-part-3-histograms/  (nice introduction)
- http://matplotlib.org/examples/pylab_examples/histogram_demo_extended.html
- http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.hist
- http://matplotlib.org/users/image_tutorial.html
"""

import numpy as np
import matplotlib.pyplot as plt

# SETUP #######################################################################

# histtype : [‘bar’ | ‘barstacked’ | ‘step’ | ‘stepfilled’]
HIST_TYPE='bar'
ALPHA=0.5

# MAKE DATA ###################################################################

x = np.array([0.3, 0.7, 1.5, 3.5])
weights = np.array([2, 1, 0.5, 1.5])

# INIT FIGURE #################################################################

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 9))

# AX1 #############

# Create a histogram by providing the bin edges: [i, i+1[
bins1 = [0., 1., 2., 3., 4., 5.]

res_tuple1 = ax1.hist(x,
                      weights=weights,
                      bins=bins1,
                      histtype=HIST_TYPE,
                      alpha=ALPHA)

ax1.set_xlabel("value")
ax1.set_ylabel("counts")
print(res_tuple1)

# AX2 #############

# Create a histogram by providing the bin edges: [i, i+1[
bins2 = [0., 0.5, 1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5, 5.]

res_tuple2 = ax2.hist(x,
                      weights=weights,
                      bins=bins2,
                      histtype=HIST_TYPE,
                      alpha=ALPHA)

ax2.set_xlabel("value")
ax2.set_ylabel("counts")
print(res_tuple2)

# SHOW AND SAVE FILE ##########################################################

plt.savefig("hist_with_weighted_values.png", bbox_inches='tight')
plt.show()
