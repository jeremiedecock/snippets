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
# - http://cairographics.org/samples/
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
    surface = cairo.SVGSurface("dash.svg", WIDTH, HEIGHT)

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
    #
    # context.set_dash()
    #   Sets the dash pattern to be used by stroke(). A dash pattern is
    #   specified by dashes - a sequence of positive values. Each value
    #   provides the length of alternate “on” and “off” portions of the stroke.
    #   The offset specifies an offset into the pattern at which the stroke
    #   begins.
    #   Each “on” segment will have caps applied as if the segment were a
    #   separate sub-path. In particular, it is valid to use an “on” length of
    #   0.0 with cairo.LINE_CAP_ROUND or cairo.LINE_CAP_SQUARE in order to
    #   distributed dots or squares along a path.
    #   Note: The length values are in user-space units as evaluated at the
    #   time of stroking. This is not necessarily the same as the user space at
    #   the time of set_dash().
    #   If the number of dashes is 0 dashing is disabled.
    #   If the number of dashes is 1 a symmetric pattern is assumed with
    #   alternating on and off portions of the size specified by the single
    #   value in dashes.

    context.set_line_width(0.01)

    context.set_source_rgb(1, 1, 1)
    context.rectangle(0, 0, 1, 1)
    context.fill()

    # STROKE

    context.set_source_rgb(0, 0, 0)

    context.set_dash((0.03,)) # ink and skip
    context.rectangle(0.1, 0.1, 0.3, 0.3)
    context.stroke()

    context.set_dash((0.04,  # ink
                      0.01)) # skip
    context.rectangle(0.1, 0.6, 0.3, 0.3)
    context.stroke()

    context.set_dash((0.03,  # ink
                      0.01,  # skip
                      0.01,  # ink
                      0.01)) # skip
    context.rectangle(0.6, 0.1, 0.3, 0.3)
    context.stroke()

    context.set_dash((0.03,  # ink
                      0.01,  # skip
                      0.01,  # ink
                      0.01,  # skip
                      0.01,  # ink
                      0.01)) # skip
    context.rectangle(0.6, 0.6, 0.3, 0.3)
    context.stroke()

    ### WRITE THE SVG FILE ###

    surface.finish()

if __name__ == '__main__':
    main()
