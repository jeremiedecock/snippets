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

# See also: http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/tkFileDialog.html
#           http://tkinter.unpythonic.net/wiki/tkFileDialog

# Intended for cases where the user wants to select an existing file. If the
# user selects a nonexistent file, a popup will appear informing them that the
# selected file does not exist. 

import os
import tkinter as tk
import tkinter.filedialog

# FILE_TYPES = [(label1, pattern1), (label2, pattern2), ...]
FILE_TYPES = [
            ('Python Source Files', '.py'),
            ('C++ Source Files', '.cpp .cc .c .h .hpp'),
            ('All Files', '.*')
        ]

HOME = os.path.expanduser("~")

root = tk.Tk()

def print_file():
    fd = open(entry.get(), "r")
    print("FILEPATH:", fd.name) # Path of the opened file
    print(fd.read())
    fd.close()

def open_file():
    path = tk.filedialog.askopenfilename(parent=root,
                                         filetypes=FILE_TYPES,     # optional
                                         defaultextension='.py',   # optional
                                         #initialdir=HOME,          # optional
                                         initialfile='hello.py',   # optional
                                         title='Select your file') # optional

    if path is not None:
        entry.delete(0, tk.END)
        entry.insert(0, path)

entry = tk.Entry(root, width=80)
entry.pack(side=tk.LEFT)

open_button = tk.Button(root, text="Open", command=open_file)
open_button.pack(side=tk.LEFT)

print_button = tk.Button(root, text="Print", command=print_file)
print_button.pack(side=tk.RIGHT)

tk.mainloop()

