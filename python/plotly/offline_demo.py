#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Source: https://plot.ly/python/getting-started/

# There are two methods for plotting offline:
# - plotly.offline.plot() to create and standalone HTML that is saved locally and opened inside your web browser.
# - plotly.offline.iplot() when working offline in a Jupyter Notebook to display the plot in the notebook.

import plotly
import plotly.graph_objs as go

plotly.offline.init_notebook_mode(connected=True)

# Use "iplot" instead of "plot" in the next line when working in a Jupyter Notebook
plotly.offline.plot({
    "data": [go.Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
    "layout": go.Layout(title="hello world")
})
