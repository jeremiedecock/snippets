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

def hello():
    print("Hello, world!")

# WINDOW 1 (there should be only one "Tk" object) #############################

window1 = tk.Tk()
window1.title("Window 1")

quit_button = tk.Button(window1, width=12, text="Quit", command=window1.quit)
quit_button.pack(side=tk.LEFT)

hello_button = tk.Button(window1, width=12, text="Hello", command=hello)
hello_button.pack(side=tk.RIGHT)

# WINDOW 2 (Toplevel object) ##################################################

window2 = tk.Toplevel()
window2.title("Window 2")
window2.geometry("+200+200")

quit_button = tk.Button(window2, width=12, text="Quit", command=window2.quit)
quit_button.pack(side=tk.LEFT)

hello_button = tk.Button(window2, width=12, text="Hello", command=hello)
hello_button.pack(side=tk.RIGHT)

# Let window2's close button quit the application
window2.protocol("WM_DELETE_WINDOW", window1.quit)

# WINDOW 3 (Toplevel object) ##################################################

window3 = tk.Toplevel()
window3.title("Window 3")
window3.geometry("+200+400")

quit_button = tk.Button(window3, width=12, text="Quit", command=window3.quit)
quit_button.pack(side=tk.LEFT)

hello_button = tk.Button(window3, width=12, text="Hello", command=hello)
hello_button.pack(side=tk.RIGHT)

# Let window3's close button quit the application
window3.protocol("WM_DELETE_WINDOW", window1.quit)

# MAIN LOOP ("Tk" object) #####################################################

window1.mainloop()
