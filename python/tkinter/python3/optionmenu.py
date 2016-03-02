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

# See also: http://effbot.org/tkinterbook/optionmenu.htm
#           http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/optionmenu.html

import tkinter as tk

root = tk.Tk()

test_var = tk.StringVar()

# Initialize
test_var.set("apple")

optionmenu = tk.OptionMenu(root, test_var, "banana", "apple", "mango", "orange")
# or
# option_list = ["banana", "apple", "mango", "orange"]
# optionmenu = tk.OptionMenu(root, test_var, *option_list)
optionmenu.pack(fill="x", pady=5)

def callback():
    print("var = ", test_var.get())

button = tk.Button(root, text="Print selection", command=callback)
button.pack(fill="x")

root.mainloop()

