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

# See also: http://effbot.org/tkinterbook/checkbutton.htm

import tkinter as tk

root = tk.Tk()

test_var = tk.IntVar()
test_var.set(2)    # Initialize

def callback():
    print("var = ", test_var.get())

# CREATE A TOPLEVEL MENU ######################################################

menubar = tk.Menu(root)

# CREATE A PULLDOWN MENU ######################################################
#
# tearoff:
#  "tearoff=1" permet à l'utilisateur de détacher le sous menu dans une
#  fenêtre à part.

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_radiobutton(label="One",   variable=test_var, value=1, command=callback)
file_menu.add_radiobutton(label="Two",   variable=test_var, value=2, command=callback)
file_menu.add_radiobutton(label="Three", variable=test_var, value=3, command=callback)

menubar.add_cascade(label="Test", menu=file_menu)

# DISPLAY THE MENU ############################################################
#
# The config method is used to attach the menu to the root window. The
# contents of that menu is used to create a menubar at the top of the root
# window. There is no need to pack the menu, since it is automatically
# displayed by Tkinter.

root.config(menu=menubar)

root.mainloop()

