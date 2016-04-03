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

SIZE = 250
DELTA = 5

FPS = 100
TIME_STEP_MS = int(1000 / FPS)

class Window():
    def __init__(self):
        # Init params
        self.keyboard_flags = {'up': False, 'down': False, 'left': False, 'right': False}

        # Make the window
        self.root = tk.Tk()
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=SIZE, height=SIZE, background="white")
        self.canvas.pack()

        # Draw the ball
        coordinates = (0, int(SIZE/2)-25, 50, int(SIZE/2)+25)
        self.ball = self.canvas.create_oval(coordinates, fill="red", width=2)

        # Set listenters (see "man bind" for more info)
        self.root.bind("<KeyPress>", self.keypress_callback)
        self.root.bind("<KeyRelease>", self.keyrelease_callback)


    def keypress_callback(self, event):
        "Update keyboard flags."

        if event.keysym == 'Up':
            self.keyboard_flags['up'] = True
        elif event.keysym == 'Down':
            self.keyboard_flags['down'] = True
        elif event.keysym == 'Left':
            self.keyboard_flags['left'] = True
        elif event.keysym == 'Right':
            self.keyboard_flags['right'] = True


    def keyrelease_callback(self, event):
        "Update keyboard flags."

        if event.keysym == 'Up':
            self.keyboard_flags['up'] = False
        elif event.keysym == 'Down':
            self.keyboard_flags['down'] = False
        elif event.keysym == 'Left':
            self.keyboard_flags['left'] = False
        elif event.keysym == 'Right':
            self.keyboard_flags['right'] = False


    def update_canvas(self):
        # Update the ball's coordinates
        coordinates = self.canvas.coords(self.ball)    # Get the ball's coordinates

        if self.keyboard_flags['up']:
            coordinates[1] = (coordinates[1] - DELTA) % SIZE
        if self.keyboard_flags['down']:
            coordinates[1] = (coordinates[1] + DELTA) % SIZE
        if self.keyboard_flags['left']:
            coordinates[0] = (coordinates[0] - DELTA) % SIZE
        if self.keyboard_flags['right']:
            coordinates[0] = (coordinates[0] + DELTA) % SIZE

        coordinates[2] = coordinates[0] + 50
        coordinates[3] = coordinates[1] + 50

        # Redraw the ball
        self.canvas.coords(self.ball, *coordinates)    # Set the ball's coordinates

        # Reschedule event in TIME_STEP_MS milli second
        self.root.after(TIME_STEP_MS, self.update_canvas)


    def run(self):
        # Schedule event in TIME_STEP_MS milli second
        self.root.after(TIME_STEP_MS, self.update_canvas)

        self.root.mainloop()


if __name__ == '__main__':
    win = Window()
    win.run()

