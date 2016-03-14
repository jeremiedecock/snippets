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

root = tk.Tk()

canvas = tk.Canvas(root, width=300, height=100, background="white")
canvas.pack(padx=10, pady=10)

# Rectangle ###################################################################

canvas.create_rectangle((10, 10, 90, 90), # coordinates: (x1, y1, x2, y2)
                        fill="orange",
                        outline="black",
                        width=2,
                        tag="square")

# Oval ########################################################################

canvas.create_oval((110, 10, 190, 90), # bbox coordinates: (x1, y1, x2, y2)
                   fill="orange",
                   outline="black",
                   width=2,
                   tag="circle")

# Polygon #####################################################################

coords = (210, 90, 250, 10, 290, 90)   # coordinates: (x1, y1, x2, y2, x3, y3)
canvas.create_polygon(coords,
                      fill="orange",
                      outline="black",
                      width=2,
                      tag="triangle")

# Bind items ##################################################################

def square_callback(event):                   # event is a tkinter.Event object
    #print("Clicked at:", event.x, event.y)
    print("You have clicked on the square")

def circle_callback(event):                   # event is a tkinter.Event object
    #print("Clicked at:", event.x, event.y)
    print("You have clicked on the circle")

def triangle_callback(event):                 # event is a tkinter.Event object
    #print("Clicked at:", event.x, event.y)
    print("You have clicked on the triangle")

canvas.tag_bind("square",          # a tag string or an item id
                "<Button-1>",      # the event descriptor
                square_callback,   # the callback function
                add=None)          # "+" to add this binding to the previous one(s) (i.e. keep the previous binding(s)) or None to replace it or them

canvas.tag_bind("circle",          # a tag string or an item id
                "<Button-1>",      # the event descriptor
                circle_callback,   # the callback function
                add=None)          # "+" to add this binding to the previous one(s) (i.e. keep the previous binding(s)) or None to replace it or them

canvas.tag_bind("triangle",        # a tag string or an item id
                "<Button-1>",      # the event descriptor
                triangle_callback, # the callback function
                add=None)          # "+" to add this binding to the previous one(s) (i.e. keep the previous binding(s)) or None to replace it or them

# Main loop ###################################################################

tk.Label(root, text="Click on shapes and watch your terminal.").pack()

root.mainloop()
