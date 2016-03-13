#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

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

# SEE: http://stackoverflow.com/questions/25480853/cairo-with-tkinter
#      http://effbot.org/tkinterbook/photoimage.htm#patterns

# Required Debian package (Debian 8.1 Jessie): python3-pil.imagetk

import tkinter as tk
import PIL.Image as pil      # PIL.Image is a module not a class...
import PIL.ImageTk as piltk  # PIL.ImageTk is a module not a class...

import cairo


if tk.TkVersion < 8.6:
    print("*" * 80)
    print("WARNING: Tk version {} is installed on your system.".format(tk.TkVersion))
    print("Tk < 8.6 only supports three file formats: GIF, PGM and PPM.")
    print("You need to install Tk >= 8.6 if you want to read JPEG and PNG images!")
    print("*" * 80)


# CAIRO

w, h = 800, 600

cairo_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
cairo_context = cairo.Context(cairo_surface)

# Draw something
cairo_context.scale(w, h)
cairo_context.rectangle(0, 0, 1, 1)
cairo_context.set_source_rgba(1, 0, 0, 0.8)
cairo_context.fill()


# TKINTER

# WARNING:
# A Tk window MUST be created before you can call PhotoImage!
# See: http://stackoverflow.com/questions/3177231/python-pil-imagetk-photoimage-is-giving-me-a-bus-error
#      http://stackoverflow.com/questions/1236540/how-do-i-use-pil-with-tkinter

root = tk.Tk()


# PIL

# WARNING:
# You must keep a reference to the image object in your Python program,
# either by storing it in a global variable, or by attaching it to another
# object!
#
# When a PhotoImage object is garbage-collected by Python (e.g. when you
# return from a function which stored an image in a local variable), the
# image is cleared even if it’s being displayed by a Tkinter widget.
#
# To avoid this, the program must keep an extra reference to the image
# object. A simple way to do this is to assign the image to a widget
# attribute, like this:
#
#    label = Label(image=tk_photo)
#    label.image = tk_photo        # keep a reference!
#    label.pack()
#
# (src: http://effbot.org/tkinterbook/photoimage.htm#patterns)
# See also http://infohost.nmt.edu/tcc/help/pubs/pil/image-tk.html

# WARNING:
# "cairo_surface.get_data()" is not yet implemented for Python3 (but it works with Python2).
# See http://www.cairographics.org/documentation/pycairo/3/reference/surfaces.html#cairo.ImageSurface.get_data
pil_image = pil.frombuffer("RGBA", (w,h), cairo_surface.get_data(), "raw", "BGRA", 0, 1)
tk_photo = piltk.PhotoImage(pil_image)


# TKINTER

label = tk.Label(root, image=tk_photo)
label.pack()

root.mainloop()
