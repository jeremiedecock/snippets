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

canvas = tk.Canvas(root, width=900, height=100, background="white")
canvas.pack(padx=10, pady=10)

# Lines #######################################################################

canvas.create_line((10, 10, 90, 90),        # coordinates: (x1, y1, x2, y2)
                   fill="black",
                   activedash=(4, 8),
                   activefill="steelblue1",
                   #activestipple=(4, 4),   # it doesn't work on Linux...
                   activewidth=4,
                   width=2)

# Polygon #####################################################################

coords = (110, 10, 190, 10, 110, 90, 190, 90)   # coordinates: (x1, y1, x2, y2, x3, y3, ...)
canvas.create_polygon(coords,
                      fill="orange",
                      outline="black",
                      activedash=(4, 8),
                      activefill="steelblue1",
                      activeoutline="chocolate",
                      #activeoutlinestipple=(4, 4),  # it doesn't work on Linux...
                      #activestipple=(4, 4),         # it doesn't work on Linux...
                      activewidth=4,
                      width=2)

# Rectangle ###################################################################

canvas.create_rectangle((210, 10, 290, 90), # coordinates: (x1, y1, x2, y2)
                        fill="orange",
                        outline="black",
                        activedash=(4, 8),
                        activefill="steelblue1",
                        activeoutline="chocolate",
                        #activeoutlinestipple=(4, 4),  # it doesn't work on Linux...
                        #activestipple=(4, 4),         # it doesn't work on Linux...
                        activewidth=4,
                        width=2)

# Oval ########################################################################

canvas.create_oval((310, 10, 390, 90),
                   fill="orange",
                   outline="black",
                   activedash=(4, 8),
                   activefill="steelblue1",
                   activeoutline="chocolate",
                   #activeoutlinestipple=(4, 4),  # it doesn't work on Linux...
                   #activestipple=(4, 4),         # it doesn't work on Linux...
                   activewidth=4,
                   width=2)

# Arc #########################################################################

canvas.create_arc((410, 10, 490, 90),
                  fill="orange",
                  outline="black",
                  start=45,         # the start angle in degrees
                  extent=225,       # the size, relative to the start angle (default is 90.0)
                  style="pieslice", # "pieslice", "chord" or "arc"
                  activedash=(4, 8),
                  activefill="steelblue1",
                  activeoutline="chocolate",
                  #activeoutlinestipple=(4, 4),  # it doesn't work on Linux...
                  #activestipple=(4, 4),         # it doesn't work on Linux...
                  activewidth=4,
                  width=2)

# Text ########################################################################

canvas.create_text((510, 10),
                   text="Hello!",
                   font="Helvetica 24 bold italic",
                   fill="gray",
                   activefill="steelblue1",
                   #activestipple=(4, 4),   # it doesn't work on Linux...
                   anchor="nw")  # n, ne, e, se, s, sw, w, nw, or center

# Image #######################################################################

img1 = tk.PhotoImage(file="jdhp_logo.png")
img2 = tk.PhotoImage(file="tux_128.png")
canvas.create_image((610, 50),
                    image=img1,
                    activeimage=img2,
                    anchor="w")  # n, ne, e, se, s, sw, w, nw, or center

# Main loop ###################################################################

root.mainloop()
