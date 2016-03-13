#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Jérémie DECOCK (http://www.jdhp.org)

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

# SEE: http://effbot.org/tkinterbook/tkinter-widget-styling.htm#font-descriptors

import tkinter as tk
import tkinter.font as tkfont

root = tk.Tk()

# Without the tkinter.font.Font class

label1 = tk.Label(root, text="Hello, world!", font="Verdana 10 bold", background="#FF0000", foreground="#000000")
label1.pack()

label2 = tk.Label(root, text="Hello, world!", font="Helvetica 16 bold italic", background="#0000FF", foreground="#FFFFFF")
label2.pack()

# Using the tkinter.font.Font class

font1 = tkfont.Font(family="Courier", size=10, weight=tkfont.BOLD, slant=tkfont.ITALIC, underline=1)
label3 = tk.Label(root, text="Hello, world!", font=font1, background="#00FF00", foreground="#000000")
label3.pack()

font2 = tkfont.Font(family="Times", size=10, weight=tkfont.BOLD, slant=tkfont.ITALIC, overstrike=1)
label4 = tk.Label(root, text="Hello, world!", font=font2, background="#FF0000", foreground="#000000")
label4.pack()

root.mainloop()
