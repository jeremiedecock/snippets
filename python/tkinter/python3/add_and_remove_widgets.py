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

import tkinter as tk

label_stack = []

def add_label():
    label = tk.Label(root, text="Label " + str(len(label_stack)))
    label.pack(side=tk.TOP)
    label_stack.append(label)

def del_label():
    # See http://stackoverflow.com/questions/3962247/python-removing-a-tkinter-frame
    #     http://stackoverflow.com/questions/12364981/how-to-delete-tkinter-widgets-from-a-window
    try:
        label = label_stack.pop()
        label.pack_forget()
        label.destroy()
    except:
        print("Empty stack.")

root = tk.Tk()

del_button = tk.Button(root, text="Del", width=10, command=del_label)
del_button.pack(side=tk.BOTTOM)

add_button = tk.Button(root, text="Add", width=10, command=add_label)
add_button.pack(side=tk.BOTTOM)

root.mainloop()

