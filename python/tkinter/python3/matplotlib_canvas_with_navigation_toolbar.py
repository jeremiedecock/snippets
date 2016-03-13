#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# See: http://matplotlib.sourceforge.net/examples/user_interfaces/embedding_in_tk.html
#      http://matplotlib.sourceforge.net/examples/user_interfaces/embedding_in_tk2.html
#      http://stackoverflow.com/questions/18675266/how-to-make-matplotlibpyplot-resizeable-with-the-tkinter-window-in-python

import matplotlib
matplotlib.use('TkAgg')

import math
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler

import tkinter as tk

# MATPLOTLIB ##################################################################

x_vec = np.arange(-10, 10, 0.01)
y_vec = np.sin(2 * 2 * np.pi * x_vec) * 1/np.sqrt(2*np.pi) * np.exp(-(x_vec**2)/2)

fig = plt.figure(figsize=(12.0, 6.0))
ax = fig.add_subplot(111)
ax.plot(x_vec, y_vec, "-", label="Test")

# Title and labels
ax.set_title(r"Test", fontsize=20)
ax.set_xlabel(r"$x$", fontsize=32)
ax.set_ylabel(r"$f(x)$", fontsize=32)

# Legend
ax.legend(loc='lower right', fontsize=20)

# TKINTER #####################################################################

root = tk.Tk()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg( canvas, root )
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def on_key_event(event):
    print('you pressed %s'%event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

button = tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=tk.BOTTOM)

# Add a callback on WM_DELETE_WINDOW event
root.protocol("WM_DELETE_WINDOW", _quit)

root.mainloop()
