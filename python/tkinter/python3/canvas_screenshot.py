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
import os
import os.path

if tk.TkVersion < 8.6:
    print("*" * 80)
    print("WARNING: Tk version {} is installed on your system.".format(tk.TkVersion))
    print("Tk < 8.6 only supports three file formats: GIF, PGM and PPM.")
    print("You need to install Tk >= 8.6 if you want to read JPEG and PNG images!")
    print("*" * 80)

class CanvasSaver:

    GS_COMMON_CMD = 'gs -dNOPAUSE -q -dEPSCrop -dBATCH '

    def __init__(self, canvas, dir_path='.', file_format='ps'):
        self.canvas = canvas
        self.dir_path = dir_path
        self.iteration = 0
        self.file_format = file_format  # 'ps', 'pdf', 'png' or 'jpeg'

    def save(self):
        # Set the screenshot filename
        self.iteration += 1
        basename = os.path.join(self.dir_path, '%05d' % self.iteration)

        # Generates a Postscript rendering of the canvas contents.
        # Images and embedded widgets are not included!
        # See https://www.tcl.tk/man/tcl8.4/TkCmd/canvas.htm#M60 for options.
        self.canvas.postscript(file=basename + '.ps', colormode='color')

        # The following commands convert PS files to JPEG or PNG on Unix
        # platforms. These commands use GhostScript (gs). Type "gs -h" in a
        # terminal to get the list of available devices on your platform.
        if self.file_format == 'pdf':
            cmd = self.GS_COMMON_CMD
            cmd += '-sDEVICE=pdfwrite '
            cmd += '-sOutputFile={0}.pdf {0}.ps'.format(basename)
            os.system(cmd)
        elif self.file_format == 'png':
            cmd = self.GS_COMMON_CMD
            cmd += '-sDEVICE=png16m '
            cmd += '-dGraphicsAlphaBits=4 -dTextAlphaBits=4 '
            cmd += '-sOutputFile={0}.png {0}.ps'.format(basename)
            os.system(cmd)
        elif self.file_format == 'jpeg':
            cmd = self.GS_COMMON_CMD
            cmd += '-sDEVICE=jpeg '
            cmd += '-dJPEGQ=100 -dGraphicsAlphaBits=4 -dTextAlphaBits=4 '
            cmd += '-sOutputFile={0}.jpeg {0}.ps'.format(basename)
            os.system(cmd)
        elif self.file_format == 'svg':
            cmd = 'inkscape {0}.ps --export-plain-svg={0}.svg'.format(basename)
            os.system(cmd)


SIZE = 300

FPS = 100
TIME_STEP_MS = int(1000 / FPS)

def main():
    """Main function"""

    root = tk.Tk()

    canvas = tk.Canvas(root, width=SIZE, height=SIZE, background="white")
    canvas.pack()
    
    # Add a background image
    img = tk.PhotoImage(file="jdhp_logo.png")
    canvas.create_image((150, 150), image=img, anchor="c")

    # Draw the ball
    coordinates = (0, int(SIZE/2)-25, 50, int(SIZE/2)+25)
    ball = canvas.create_oval(coordinates, fill="red", width=2)

    saver = CanvasSaver(canvas, file_format='pdf')

    def update_canvas():
        # Update the ball's coordinates
        coordinates = canvas.coords(ball)    # Get the ball's coordinates
        coordinates[0] = (coordinates[0] + 1) % SIZE
        coordinates[2] = coordinates[0] + 50

        # Redraw the ball
        canvas.coords(ball, *coordinates)    # Set the ball's coordinates

        # Save the canvas
        saver.save()

        # Reschedule event in TIME_STEP_MS milli second
        root.after(TIME_STEP_MS, update_canvas)

    # Schedule event in TIME_STEP_MS milli second
    root.after(TIME_STEP_MS, update_canvas)

    root.mainloop()

if __name__ == '__main__':
    main()
