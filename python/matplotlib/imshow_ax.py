#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Display data as an image (via AxesSubplot)

See: http://matplotlib.org/examples/pylab_examples/image_demo.html

See also:

- http://matplotlib.org/examples/color/colormaps_reference.html (the list of all colormaps)
- http://matplotlib.org/users/colormaps.html?highlight=colormap#mycarta-banding (what is the right colormap to choose for a given plot)
"""

import numpy as np
import matplotlib.pyplot as plt

# MAKE DATAS ##################################################################

z_matrix = np.array([[xi * yi for xi in range(50)] for yi in range(50)])

# PLOT ########################################################################
# The list of all colormaps: http://matplotlib.org/examples/color/colormaps_reference.html

#interp='nearest'     # "raw" (non smooth) map
interp = 'bilinear'   # "smooth" map

fig = plt.figure()
ax = fig.add_subplot(111)

im = ax.imshow(z_matrix, interpolation=interp, origin='lower')

plt.colorbar(im) # draw the colorbar

# SAVE AND SHOW ###############################################################

plt.savefig("imshow_ax.png")
plt.show()
