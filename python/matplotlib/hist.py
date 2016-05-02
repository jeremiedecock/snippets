#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See:
# - http://bespokeblog.wordpress.com/2011/07/11/basic-data-plotting-with-matplotlib-part-3-histograms/  (nice introduction)
# - http://matplotlib.org/examples/pylab_examples/histogram_demo_extended.html
# - http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.hist
# - http://matplotlib.org/users/image_tutorial.html

import numpy as np
import matplotlib.pyplot as plt

# SETUP #######################################################################

# histtype : [‘bar’ | ‘barstacked’ | ‘step’ | ‘stepfilled’]
HIST_TYPE='bar'
ALPHA=0.5

# MAKE DATA ###################################################################

gaussian_numbers_list_1 = np.random.normal(size=1000)
gaussian_numbers_list_2 = np.random.normal(size=500)
gaussian_numbers_list_3 = np.random.normal(size=500)

# INIT FIGURE #################################################################

fig = plt.figure(figsize=(16.0, 9.0))

ax1 = fig.add_subplot(411)
ax2 = fig.add_subplot(412)
ax3 = fig.add_subplot(413)
ax4 = fig.add_subplot(414)

# AX1 #########################################################################

res_tuple = ax1.hist(gaussian_numbers_list_1, histtype=HIST_TYPE, alpha=ALPHA)
print(res_tuple)

res_tuple = ax1.hist(gaussian_numbers_list_1, bins=35, histtype=HIST_TYPE, alpha=ALPHA)
ax1.set_xlabel("value")
ax1.set_ylabel("frequency")
print(res_tuple)

# AX2 #########################################################################

# Create a histogram by providing the bin edges (equally spaced here)
bins = [-4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
res_tuple = ax2.hist(gaussian_numbers_list_1, bins=bins, histtype=HIST_TYPE)
ax2.set_xlabel("value")
ax2.set_ylabel("frequency")
print(res_tuple)

# AX3 #########################################################################

res_tuple = ax3.hist(gaussian_numbers_list_1, bins=30, histtype=HIST_TYPE, normed=True, cumulative=True)
ax3.set_ylim([0., 1.])
ax3.set_xlabel("value")
ax3.set_ylabel("probability")
print(res_tuple)

# AX4 #########################################################################

res_tuple = ax4.hist([gaussian_numbers_list_1, gaussian_numbers_list_2, gaussian_numbers_list_3], bins=30, histtype=HIST_TYPE)
ax4.set_xlabel("value")
ax4.set_ylabel("frequency")
print(res_tuple)

# SHOW AND SAVE FILE ##########################################################

plt.tight_layout()

plt.savefig("hist.png")
plt.show()
