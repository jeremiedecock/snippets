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

canvas = tk.Canvas(root, width=600, height=600)
canvas.pack(padx=10, pady=10)

# arrow: "none", "first", "last" or "both"
canvas.create_line((0, 0, 200, 100), fill="red", width=4, dash=(8, 4), arrow="last", arrowshape=(16, 20, 6))
canvas.create_line((0, 100, 200, 0), fill="black", width=2)

canvas.create_rectangle((300, 0, 500, 100), outline="orange", fill="blue", width=2)

canvas.create_oval((0, 200, 200, 300), outline="purple", fill="yellow", width=2)

# start: the start angle in degrees
# extent: the size, relative to the start angle. Default is 90.0
# style: "pieslice", "chord" or "arc"
canvas.create_arc((300, 200, 500, 300), start=45, extent=225, style="arc", outline="brown", width=2)

canvas.create_polygon((0, 400, 50, 450, 100, 400, 150, 450), fill="black", width=2)

canvas.create_text((0, 500), text="Hello!", font="Helvetica 32 bold italic", fill="gray", anchor="w")

img = tk.PhotoImage(file="jdhp_logo.png")
canvas.create_image((300, 500), image=img, anchor="w")

root.mainloop()
