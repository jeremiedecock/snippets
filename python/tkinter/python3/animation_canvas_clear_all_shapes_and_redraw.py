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

# WARNING: keeping shapes instances like in
# animation_canvas_update_shapes_instances.py is probably a better solution...

import tkinter as tk

SIZE = 250

FPS = 100
TIME_STEP_MS = int(1000 / FPS)

POSITION = 0

###

root = tk.Tk()

canvas = tk.Canvas(root, width=SIZE, height=SIZE, background="white")
canvas.pack()

def update_canvas():
    # Update the ball's position
    global POSITION
    POSITION = (POSITION + 1) % SIZE

    # Clear the canvas (remove all shapes)
    canvas.delete(tk.ALL)

    # Or...
    #for tag in canvas.find_all():
    #    canvas.delete(tag)

    # Draw the ball
    canvas.create_oval(POSITION,
                       int(SIZE/2)-25,
                       POSITION + 50,
                       int(SIZE/2)+25,
                       fill="red",
                       width=2)

    # Reschedule event in TIME_STEP_MS milli second
    root.after(TIME_STEP_MS, update_canvas)

# Schedule event in TIME_STEP_MS milli second
root.after(TIME_STEP_MS, update_canvas)

root.mainloop()
