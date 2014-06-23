#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)

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


# SEE:
# - http://cairographics.org/documentation/pycairo/3/reference/index.html
# - http://cairographics.org/pycairo/tutorial/
# - http://www.tortall.net/mu/wiki/CairoTutorial

import gtk
import math

WIDTH, HEIGHT = 256, 256

class Window(gtk.Window):

    def __init__(self):
        super(Window, self).__init__()

        self.set_title("GTK and Cairo")
        self.resize(WIDTH, HEIGHT)
        self.set_position(gtk.WIN_POS_CENTER)

        self.connect("destroy", gtk.main_quit)

        drawing_area = gtk.DrawingArea()
        drawing_area.connect("expose-event", self.expose)
        self.add(drawing_area)

        self.show_all()

    def expose(self, widget, event):

        context = widget.window.cairo_create()

        # Normalizing the canvas ([0,1],[0,1]) -> ([0,WIDTH],[0,HEIGHT])
        context.scale(WIDTH, HEIGHT)

        # DRAW LINES

        context.set_source_rgb(0, 0, 0)
        context.move_to(0, 0)
        context.line_to(1, 1)
        context.move_to(1, 0)
        context.line_to(0, 1)
        context.set_line_width(0.2)
        context.stroke()

        # DRAW RECTANGLES

        context.set_source_rgba(1, 0, 0, 0.80)
        context.rectangle(0, 0, 0.5, 0.5)
        context.fill()

        context.set_source_rgba(0, 1, 0, 0.60)
        context.rectangle(0, 0.5, 0.5, 0.5)
        context.fill()

        context.set_source_rgba(0, 0, 1, 0.40)
        context.rectangle(0.5, 0, 0.5, 0.5)
        context.fill()

def main():
    """Main function"""

    window = Window()
    gtk.main()

if __name__ == '__main__':
    main()
