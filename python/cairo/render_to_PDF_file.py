#!/usr/bin/env python3
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

import cairo
import math

WIDTH, HEIGHT = 256, 256

def main():
    """Main function"""

    # Image surfaces provide the ability to render to memory buffers either
    # allocated by cairo or by the calling code.
    # List of supported surfaces: http://www.cairographics.org/manual/cairo-surfaces.html
    surface = cairo.PDFSurface("test.pdf", WIDTH, HEIGHT)

    # cairo.Context is the object that you send your drawing commands to.
    context = cairo.Context(surface)

    # Normalizing the canvas ([0,1],[0,1]) -> ([0,WIDTH],[0,HEIGHT])
    context.scale(WIDTH, HEIGHT)

    ### DRAW ###
     
    # context.set_source_rgb(0., 0., 0.)
    # context.set_source_rgba(0., 0., 0., 1.)
    #   Sets the source pattern within context to an opaque color. This opaque color
    #   will then be used for any subsequent drawing operation until a new source
    #   pattern is set.
    #   The color components are floating point numbers in the range 0 to 1. If
    #   the values passed in are outside that range, they will be clamped.
    #   The default source pattern is opaque black, (that is, it is equivalent to
    #   cairo_set_source_rgb(context, 0.0, 0.0, 0.0)).
    #   Using set_source_rgb(r, g, b) is equivalent to using
    #   set_source_rgba(r, g, b, 1.0), and it sets your source color to use
    #   full opacity. 
    #
    # context.stroke()
    #   The stroke() operation takes a virtual pen along the current path
    #   according to the current line width, line join, line cap, and dash
    #   settings. After cairo_stroke(), the current path will be cleared from
    #   the cairo context.
    #   See http://www.cairographics.org/manual/cairo-cairo-t.html#cairo-stroke
    #
    # context.fill()
    #   A drawing operator that fills the current path according to the current
    #   fill rule, (each sub-path is implicitly closed before being filled).
    #   After cairo_fill(), the current path will be cleared from the cairo
    #   context.
    #   See http://www.cairographics.org/manual/cairo-cairo-t.html#cairo-fill

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

    ### WRITE THE SVG FILE ###

    surface.finish()

if __name__ == '__main__':
    main()
