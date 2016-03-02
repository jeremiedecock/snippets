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

# See also: http://effbot.org/tkinterbook/listbox.htm

import tkinter as tk

root = tk.Tk()

# LISTBOX #############################

# The "selectmode" can be:
# - SINGLE:   just a single choice
# - BROWSE:   same, but the selection can be moved using the mouse
# - MULTIPLE: multiple item can be choosen, by clicking at them one at a
#             time
# - EXTENDED: multiple ranges of items can be chosen, using the Shift and
#             Control keyboard modifiers
listbox = tk.Listbox(root, selectmode=tk.EXTENDED)
listbox.pack()

items = ["banana", "apple", "mango", "orange"]

for item in items:
    listbox.insert(tk.END, item)

# BUTTON ##############################

def print_selection():
    selection_id_tuple = listbox.curselection()
    selection_label_tuple = tuple(listbox.get(item) for item in selection_id_tuple)
    print(selection_id_tuple)
    print(selection_label_tuple)

button = tk.Button(root, text="Print selection", width=15, command=print_selection)
button.pack()

# MAIN LOOP ###########################

root.mainloop()

