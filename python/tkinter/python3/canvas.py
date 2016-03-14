#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

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

if tk.TkVersion < 8.6:
    print("*" * 80)
    print("WARNING: Tk version {} is installed on your system.".format(tk.TkVersion))
    print("Tk < 8.6 only supports three file formats: GIF, PGM and PPM.")
    print("You need to install Tk >= 8.6 if you want to read JPEG and PNG images!")
    print("*" * 80)

root = tk.Tk()

canvas = tk.Canvas(root, width=700, height=700, background="white")
canvas.pack(padx=10, pady=10)

# Lines #######################################################################

canvas.create_line((10, 10, 90, 90),        # coordinates: (x1, y1, x2, y2)
                   fill="red",
                   width=4,
                   dash=(8, 4),
                   arrow="last",            # "none", "first", "last" or "both"
                   arrowshape=(16, 20, 6))

canvas.create_line((110, 10, 190, 90),      # coordinates: (x1, y1, x2, y2)
                   fill="black",
                   width=2)

coords = (210, 10, 250, 90, 290, 10)   # coordinates: (x1, y1, x2, y2, x3, y3)
canvas.create_line(coords,
                   fill="black",
                   width=5,
                   joinstyle="round")
canvas.create_line(coords,
                   fill="red",
                   width=2,
                   smooth=True)

coords = (310, 10, 330, 90, 350, 10, 370, 90, 390, 10)   # coordinates: (x1, y1, x2, y2, x3, y3, ...)
canvas.create_line(coords,
                   fill="black",
                   width=2)
canvas.create_line(coords,
                   fill="red",
                   width=5,
                   smooth=True)

coords = (410, 10, 450, 10, 450, 90, 490, 90)   # coordinates: (x1, y1, x2, y2, x3, y3, ...)
canvas.create_line(coords,
                   fill="black",
                   dash=(2, 2),
                   width=2,
                   joinstyle="round")
canvas.create_line(coords,
                   fill="red",
                   width=2,
                   smooth=True)

# Polygon #####################################################################

coords = (110, 110, 190, 110, 110, 190, 190, 190)   # coordinates: (x1, y1, x2, y2, x3, y3, ...)
canvas.create_polygon(coords,
                      fill="orange",
                      outline="black",
                      width=2,
                      dash=(2, 4),
                      joinstyle="round")

coords = (210, 110, 250, 190, 290, 110)   # coordinates: (x1, y1, x2, y2, x3, y3)
canvas.create_polygon(coords,
                      fill="red",
                      outline="black",
                      width=5,
                      joinstyle="round")

coords = (310, 110, 330, 190, 350, 150, 370, 190, 390, 110)   # coordinates: (x1, y1, x2, y2, x3, y3, ...)
canvas.create_polygon(coords,
                      fill="red",
                      activefill="blue",
                      outline="black",
                      width=2,
                      joinstyle="round")

coords = (410, 110, 430, 190, 450, 150, 470, 190, 490, 110)   # coordinates: (x1, y1, x2, y2, x3, y3, ...)
canvas.create_polygon(coords,
                      fill="red",
                      activefill="blue",
                      outline="black",
                      width=2,
                      smooth=True,
                      joinstyle="round")

# Rectangle ###################################################################

canvas.create_rectangle((10, 210, 90, 290), # coordinates: (x1, y1, x2, y2)
                        outline="orange",
                        fill="blue",
                        width=2)

canvas.create_rectangle((110, 210, 190, 290), # coordinates: (x1, y1, x2, y2)
                        outline="black",
                        dash=(12, 6),
                        width=2)

# Oval ########################################################################

canvas.create_oval((210, 210, 290, 290),
                   outline="purple",
                   fill="yellow",
                   width=2)

canvas.create_oval((310, 210, 390, 290),
                   outline="black",
                   dash=(6, 12),
                   fill="pink",
                   width=2)

canvas.create_oval((410, 210, 590, 290),
                   outline="pink",
                   fill="green",
                   width=2)

# Arc #########################################################################

canvas.create_arc((10, 310, 90, 390),
                  start=45,        # the start angle in degrees
                  extent=225,      # the size, relative to the start angle (default is 90.0)
                  style="arc",     # "pieslice", "chord" or "arc"
                  outline="brown",
                  width=2)

# Text ########################################################################

canvas.create_rectangle((10, 410, 90, 490), # coordinates: (x1, y1, x2, y2)
                        outline="gray75",
                        dash=(4, 4),
                        width=2)

canvas.create_text((10, 410),
                   text="Hello!",
                   font="Helvetica 24 bold italic",
                   fill="gray",
                   anchor="nw")  # n, ne, e, se, s, sw, w, nw, or center

# Image #######################################################################

img = tk.PhotoImage(file="jdhp_logo.png")
canvas.create_image((10, 610),
                    image=img,
                    anchor="w")  # n, ne, e, se, s, sw, w, nw, or center

# Main loop ###################################################################

root.mainloop()
