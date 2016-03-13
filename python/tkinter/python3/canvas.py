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

# See: http://effbot.org/tkinterbook/canvas.htm

import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=600, background="white")
canvas.pack(padx=10, pady=10)

# Lines #######################################################################

# arrow: "none", "first", "last" or "both"
canvas.create_line((10, 10, 90, 90),        # coordinates: (x1, y1, x2, y2)
                   fill="red",
                   width=4,
                   dash=(8, 4),
                   arrow="last",
                   arrowshape=(16, 20, 6))

canvas.create_line((110, 10, 190, 90),      # coordinates: (x1, y1, x2, y2)
                   fill="black",
                   width=2)

coords1 = (210, 10, 250, 90, 290, 10)   # coordinates: (x1, y1, x2, y2, x3, y3)
canvas.create_line(coords1,
                   fill="black",
                   width=5,
                   joinstyle="round")
canvas.create_line(coords1,
                   fill="red",
                   width=2,
                   smooth=1)

coords2 = (310, 10, 330, 90, 350, 10, 370, 90, 390, 10)   # coordinates: (x1, y1, x2, y2, x3, y3, ...)
canvas.create_line(coords2,
                   fill="black",
                   width=2)
canvas.create_line(coords2,
                   fill="red",
                   width=5,
                   smooth=1)

# Polygon #####################################################################

coords3 = (210, 110, 250, 190, 290, 110)   # coordinates: (x1, y1, x2, y2, x3, y3)
canvas.create_polygon(coords3,
                      fill="red",
                      outline="black",
                      width=5,
                      joinstyle="round")

coords4 = (310, 110, 330, 190, 350, 150, 370, 190, 390, 110)   # coordinates: (x1, y1, x2, y2, x3, y3, ...)
canvas.create_polygon(coords4,
                      fill="red",
                      activefill="blue",
                      outline="black",
                      width=2,
                      joinstyle="round")

# Rectangle ###################################################################

canvas.create_rectangle((410, 110, 490, 190), # coordinates: (x1, y1, x2, y2)
                        outline="orange",
                        fill="blue",
                        width=2)

# Oval ########################################################################

canvas.create_oval((0, 200, 200, 300), outline="purple", fill="yellow", width=2)

canvas.create_arc((300, 200, 500, 300),
                  start=45,        # the start angle in degrees
                  extent=225,      # the size, relative to the start angle (default is 90.0)
                  style="arc",     # "pieslice", "chord" or "arc"
                  outline="brown",
                  width=2)

canvas.create_polygon((0, 400, 50, 450, 100, 400, 150, 450), fill="black", width=2)

canvas.create_text((0, 500), text="Hello!", font="Helvetica 32 bold italic", fill="gray", anchor="w")

img = tk.PhotoImage(file="jdhp_logo.png")
canvas.create_image((300, 500), image=img, anchor="w")

root.mainloop()
