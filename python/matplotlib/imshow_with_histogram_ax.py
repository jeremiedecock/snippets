#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Display an image and its histogram

See: http://matplotlib.org/examples/pylab_examples/image_demo.html

See also:

- http://matplotlib.org/examples/color/colormaps_reference.html (the list of all colormaps)
- http://matplotlib.org/users/colormaps.html?highlight=colormap#mycarta-banding (what is the right colormap to choose for a given plot)
"""

import PIL.Image as pil_img     # PIL.Image is a module not a class...

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# SETUP #######################################################################

# histtype : [‘bar’ | ‘barstacked’ | ‘step’ | ‘stepfilled’]
HIST_TYPE='bar'

#interp='nearest'     # "raw" (non smooth) map
INTERP = 'bilinear'   # "smooth" map

# MAKE DATAS ##################################################################

img_array = np.array(pil_img.open("test.jpeg").convert('L'))

# INIT FIGURE #################################################################

fig = plt.figure()

ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# AX1 #########################################################################

# nparray.ravel(): Return a flattened array.
values, bins, patches = ax1.hist(img_array.ravel(),
                                 histtype=HIST_TYPE,
                                 bins=255,
                                 #bins=img_array.max() - img_array.min(),
                                 #range=(0., 255.),
                                 fc='k',
                                 ec='k')

print("values:", values)
print("bins:", bins)
print("patches:", patches)

ax1.set_xlim([0., 255.])
#ax1.set_xlim([img_array.min(), img_array.max(])

# AX2 #########################################################################

im = ax2.imshow(img_array,
                interpolation=INTERP,
                origin='upper',
                cmap='gray')

plt.colorbar(im) # draw colorbar

# SAVE AND SHOW ###############################################################

plt.savefig("imshow_with_histogram_ax.png")
plt.show()
