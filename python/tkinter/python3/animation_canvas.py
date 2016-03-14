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

# See also: http://effbot.org/tkinterbook/widget.htm
#           http://effbot.org/tkinterbook/canvas.htm

import tkinter as tk
import random

SIZE = 500

MAX_LINES = 20

###

root = tk.Tk()

canvas = tk.Canvas(root, width=SIZE, height=SIZE, background="white")
canvas.pack()

def update_canvas():
    # Clear the canvas if there are too many lines
    if len(canvas.find_all()) > MAX_LINES:
        canvas.delete(tk.ALL)  # or canvas.delete("all")

    # Add a line
    canvas.create_line(random.randint(0, SIZE),
                       random.randint(0, SIZE),
                       random.randint(0, SIZE),
                       random.randint(0, SIZE))

    # Reschedule event in 100 milli seconds
    root.after(100, update_canvas)

# Schedule event in 100 milli seconds
root.after(100, update_canvas)

root.mainloop()
