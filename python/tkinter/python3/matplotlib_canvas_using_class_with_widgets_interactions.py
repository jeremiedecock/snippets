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

SCALE_MIN = 0.
SCALE_MAX = 2. * np.pi

class Gui:

    def __init__(self, root):

        # Matplotlib ##################

        self.fig = plt.figure(figsize=(6.0, 6.0))

        # Make widgets ################

        self.root = root

        # Add a callback on WM_DELETE_WINDOW events
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Label
        tk.Label(self.root, text="Phase:").pack(anchor="w")

        # Scale
        self.scale = tk.Scale(self.root,
                              from_=SCALE_MIN,
                              to=SCALE_MAX,
                              resolution=0.01,
                              orient=tk.HORIZONTAL,
                              command=self.scale_callback)
        self.scale.pack(fill="x", expand=True)

        self.scale.set(SCALE_MIN)            # Set the scale value

        # Draw the figure #############

        self.draw_figure()


    def scale_callback(self, ev=None):
        """
        Called when the scale widget is moved.
        """
        print(self.scale.get())    # Get the scale value (integer or float)
        self.draw_figure()


    def draw_figure(self):
        """
        Draw the figure.
        """
        self.fig.clf()
        
        ax = self.fig.add_subplot(111)

        phase = self.scale.get()
        x = np.arange(0, 4. * np.pi, 0.05)
        y = np.sin(x + phase)
        ax.plot(x, y)

        ax.set_xlim([0, 4. * np.pi])

        self.fig.canvas.draw()


    def run(self):
        """
        Launch the main loop (Tk event loop).
        """
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
