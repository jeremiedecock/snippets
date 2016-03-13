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

# WARNING: this snippet doesn't work on MacOSX (Tk 8.6)!

import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=600, background="white")
canvas.pack(padx=10, pady=10)

canvas.create_rectangle((100, 100, 300, 300), outline="black", fill="red", width=5, stipple="gray75", outlinestipple="gray75")
canvas.create_rectangle((200, 200, 400, 400), outline="black", fill="red", width=5, stipple="gray50", outlinestipple="gray50")
canvas.create_rectangle((300, 300, 500, 500), outline="black", fill="red", width=5, stipple="gray25", outlinestipple="gray25")

root.mainloop()
