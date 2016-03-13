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

# See: http://effbot.org/tkinterbook/frame.htm
# Inspired by: http://www.java2s.com/Code/Python/GUI-Tk/DefineGUIinaclass.htm

import tkinter as tk

root = tk.Tk()
root.title("Frame styles")

relief_tuple = ("raised", "sunken", "flat", "ridge", "groove", "solid")

for border_width in range(5):

    label = tk.Label(root, text="border width = {}".format(border_width))
    label.grid(padx=5, pady=5, row=border_width, column=0)

    for index, relief_str in enumerate(relief_tuple):

        frame = tk.Frame(root,
                         bd=border_width,     # border width
                         relief=relief_str)

        frame.grid(padx=5, pady=5, row=border_width, column=index+1)

        label = tk.Label(frame, text=relief_str)
        label.pack()

root.mainloop()
