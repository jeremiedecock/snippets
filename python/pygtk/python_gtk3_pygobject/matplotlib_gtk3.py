#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: http://gtk3-matplotlib-cookbook.readthedocs.org/en/latest/
     http://matplotlib.org/1.4.2/examples/user_interfaces/index.html
"""

from gi.repository import Gtk as gtk

import numpy as np
import matplotlib.pyplot as plt

# WARNING!!!
#  The FigureCanvasGTK3Agg rendering backend may be broken.
#  Try FigureCanvasGTK3Cairo instead (see matplotlib_cairo.py).
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

def main():
    window = gtk.Window()
    window.set_default_size(800, 600)

    # matplotlib
    x_vec = np.arange(-10, 10, 0.01)
    y_vec = np.sin(2 * 2 * np.pi * x_vec) * 1/np.sqrt(2*np.pi) * np.exp(-(x_vec**2)/2)

    #fig = plt.figure(figsize=(8.0, 6.0), dpi=100)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x_vec, y_vec)

    # add the image to the window
    scrolled_window = gtk.ScrolledWindow()
    window.add(scrolled_window)

    canvas = FigureCanvas(fig)
    canvas.set_size_request(800, 600)             # optional...
    scrolled_window.add_with_viewport(canvas)

    # main
    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

