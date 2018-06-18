#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Source: https://plot.ly/matplotlib/

# There are two methods for plotting offline:
# - plotly.offline.plot_mpl() to create and standalone HTML that is saved locally and opened inside your web browser.
# - plotly.offline.iplot_mpl() when working offline in a Jupyter Notebook to display the plot in the notebook.

import numpy as np
import matplotlib.pyplot as plt
import plotly

n = 50
x, y, z, s, ew = np.random.rand(5, n)
c, ec = np.random.rand(2, n, 4)
area_scale, width_scale = 500, 5

fig, ax = plt.subplots()
sc = ax.scatter(x, y, c=c,
                s=np.square(s)*area_scale,
                edgecolor=ec,
                linewidth=ew*width_scale)
ax.grid()

# Use "iplot_mpl" instead of "plot_mpl" in the next line when working in a Jupyter Notebook
plot_url = plotly.offline.plot_mpl(fig)
