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

# Inspired by http://www.labri.fr/perso/nrougier/teaching/matplotlib/matplotlib.html#animation
# See also: http://effbot.org/tkinterbook/widget.htm

import tkinter as tk
import random

SIZE = 500

MIN_RADIUS = 15
MAX_RADIUS = 30

NUM_CIRCLES = 50

FPS = 25
TIME_STEP_MS = int(1000 / FPS)

def main():
    """Main function"""

    root = tk.Tk()

    canvas = tk.Canvas(root, width=SIZE, height=SIZE, background="white")
    canvas.pack()

    for index in range(NUM_CIRCLES):
        x = random.randint(0, SIZE)
        y = random.randint(0, SIZE)
        radius = random.randint(MIN_RADIUS, MAX_RADIUS)
        canvas.create_oval(x - radius,
                           y - radius,
                           x + radius,
                           y + radius,
                           width=1)

    def update_canvas():
        # Update all circles
        for tag in canvas.find_all():
            coordinates = canvas.coords(tag)    # Get the circle's coordinates
            diameter = coordinates[2] - coordinates[0]

            if diameter < 2 * MAX_RADIUS:
                coordinates[0] -= 1
                coordinates[1] -= 1
                coordinates[2] += 2
                coordinates[3] += 2
            else:
                x = random.randint(0, SIZE)
                y = random.randint(0, SIZE)
                coordinates[0] = x - MIN_RADIUS
                coordinates[1] = y - MIN_RADIUS
                coordinates[2] = x + MIN_RADIUS
                coordinates[3] = y + MIN_RADIUS
                diameter = coordinates[2] - coordinates[0]

            # Redraw the ball
            canvas.coords(tag, *coordinates)       # Change coordinates

            alpha = int(100. * diameter / (2. * MAX_RADIUS))
            color = "gray" + str(alpha)
            canvas.itemconfig(tag, outline=color)  # Change color

        # Reschedule event in TIME_STEP_MS ms
        root.after(TIME_STEP_MS, update_canvas)

    # Schedule event in TIME_STEP_MS ms
    root.after(TIME_STEP_MS, update_canvas)

    root.mainloop()

if __name__ == '__main__':
    main()
