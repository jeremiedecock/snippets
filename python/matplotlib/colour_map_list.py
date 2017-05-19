#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
List available colormaps

See: http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html

See also:

- http://matplotlib.org/examples/color/colormaps_reference.html (the list of all colormaps)
- http://matplotlib.org/users/colormaps.html?highlight=colormap#mycarta-banding (what is the right colormap to choose for a given plot)
"""

import matplotlib.pyplot as plt

# Get a list of the colormaps in matplotlib. 
maps = sorted(plt.cm.datad)

print(maps)
