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

# See: https://github.com/jeremiedecock/pyarm/blob/master/pyarm/gui/tkinter_gui.py
#      http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html
#      http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm

import tkinter as tk


def keypress_callback(event):
    if event.keysym == "Up":
        print("keypress: <Up>")
    elif event.keysym == "Down":
        print("keypress: <Down>")
    elif event.keysym == "Left":
        print("keypress: <Left>")
    elif event.keysym == "Right":
        print("keypress: <Right>")
    elif event.keysym == "Return":
        print("keypress: <Return>")
    elif event.keysym == "Escape":
        print("keypress: <Escape>")


def main():
    """Main function"""

    root = tk.Tk()

    label = tk.Label(root, text="Press some keys", width=50, height=10)
    label.pack()

    # SETUP KEYBOARD EVENT CALLBACKS
    root.bind("<Up>", keypress_callback)
    root.bind("<Down>", keypress_callback)
    root.bind("<Left>", keypress_callback)
    root.bind("<Right>", keypress_callback)
    root.bind("<Return>", keypress_callback)
    root.bind("<Escape>", keypress_callback)

    root.mainloop()

if __name__ == '__main__':
    main()
