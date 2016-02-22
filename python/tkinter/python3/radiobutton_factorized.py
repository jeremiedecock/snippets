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

# See also: http://effbot.org/tkinterbook/radiobutton.htm

import tkinter as tk

root = tk.Tk()

# Each group of Radiobutton widgets should be associated with single variable.
# Each button then represents a single value for that variable.
test_var = tk.StringVar()

# Initialize
test_var.set("apple")

def callback():
    print("var = ", test_var.get())

ITEMS = [
            ("Banana", "banana"),
            ("Apple", "apple"),
            ("Mango", "mango"),
            ("Pear", "pear")
        ]

for label, value in ITEMS:
    radiobutton = tk.Radiobutton(root, text=label, variable=test_var, value=value, command=callback)
    radiobutton.pack(anchor=tk.W)

root.mainloop()

