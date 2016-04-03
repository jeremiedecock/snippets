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

# See http://fr.slideshare.net/r1chardj0n3s/tkinter-does-not-suck (slides 83)

import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack(fill="both", expand=True)

LAST_X = None
LAST_Y = None

def callback(event):
    print("Clicked at:", event.x, event.y)

    global LAST_X
    global LAST_Y

    if (LAST_X is not None) and (LAST_Y is not None):
        canvas.create_line(LAST_X,
                           LAST_Y,
                           event.x,
                           event.y)

    LAST_X = event.x
    LAST_Y = event.y

# Available mouse events:
# - Mouse button: <Button-1>, <Button-2>, <Button-3>
# - Mouse drag: <B1-Motion>
# - Mouse release: <ButtonRelease-1>, ...
# - Double click: <Double-Button-1>, ...
# - Trible click: <Triple-Button-1>, ...
# - Mouse entered: <Enter>
# - Mouse left: <Leave>
canvas.bind("<Button-1>", callback)

root.mainloop()
