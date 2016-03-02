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

# See also: http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/tkFileDialog.html
#           http://tkinter.unpythonic.net/wiki/tkFileDialog

# Intended for cases where the user wants to select an existing file. If the
# user selects a nonexistent file, a popup will appear informing them that the
# selected file does not exist. 

import os
import tkinter as tk
import tkinter.filedialog

HOME = os.path.expanduser("~")

root = tk.Tk()

def open_file():
    path = tk.filedialog.askdirectory(parent=root,
                                      initialdir=HOME,               # optional
                                      mustexist=True,                # optional
                                      title='Select your directory') # optional

    print("PATH:", path)


open_button = tk.Button(root, text="Select a directory", command=open_file)
open_button.pack()

tk.mainloop()

