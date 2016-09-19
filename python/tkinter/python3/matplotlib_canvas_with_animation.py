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

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
import time

DELTA_TIME_MS = 100

class Gui:

    def __init__(self, root):

        # Matplotlib ##################

        self.fig = plt.figure(figsize=(8.0, 8.0))

        # Make widgets ################

        self.root = root

        # Add a callback on WM_DELETE_WINDOW events
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Draw the figure #############

        self.draw_figure()


    def update_canvas(self):
        # Draw the figure
        self.draw_figure()

        # Reschedule event in DELTA_TIME_MS milli seconds
        self.root.after(DELTA_TIME_MS, self.update_canvas)


    def draw_figure(self):
        """
        Draw the figure.
        """
        self.fig.clf()
        
        ax = self.fig.add_subplot(111)

        t = time.time() % (2. * np.pi)
        x = np.arange(-10, 10, 0.01)
        y = np.sin(x + t)
        ax.plot(x, y)

        self.fig.canvas.draw()


    def run(self):
        """
        Launch the main loop (Tk event loop).
        """
        # Schedule event in DELTA_TIME_MS milli seconds
        self.root.after(DELTA_TIME_MS, self.update_canvas)

        # Launch the main loop
        self.root.mainloop()


    def quit(self):
        """
        Clean exit.
        """
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
                             # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def main():
    root = tk.Tk()
    gui = Gui(root)
    gui.run()


if __name__ == "__main__":
    main()
