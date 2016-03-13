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

# See: http://effbot.org/tkinterbook/menu.htm
#      http://effbot.org/tkinterbook/tkinter-application-windows.htm

# TOPLEVEL MENUS:
#  "Toplevel menus are displayed just under the title bar of the root or any
#  other toplevel windows (or on Macintosh, along the upper edge of the screen).
#  To create a toplevel menu, create a new Menu instance, and use add methods to
#  add commands and other menu entries to it."

# PULLDOWN MENUS:
#  "Pulldown menus (and other submenus) are created in a similar fashion. The
#  main difference is that they are attached to a parent menu (using
#  add_cascade), instead of a toplevel window."

import tkinter as tk

root = tk.Tk()

# The callback

def hello():
    print("Hello!")

# Create a toplevel menu

menubar = tk.Menu(root)

# Create a pulldown menu
#
# tearoff:
#  "tearoff=1" permet à l'utilisateur de détacher le sous menu dans une
#  fenêtre à part.

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Open...", command=hello)
file_menu.add_command(label="Save As...", command=hello)
file_menu.add_command(label="Save", command=hello)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=file_menu)

# Create a pulldown menu

edit_menu = tk.Menu(menubar, tearoff=0)
edit_menu.add_command(label="Cut", command=hello)
edit_menu.add_command(label="Copy", command=hello)
edit_menu.add_command(label="Paste", command=hello)

menubar.add_cascade(label="Edit", menu=edit_menu)

# Create a pulldown menu

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About...", command=hello)

menubar.add_cascade(label="Help", menu=help_menu)

# Display the menu
# The config method is used to attach the menu to the root window. The
# contents of that menu is used to create a menubar at the top of the root
# window. There is no need to pack the menu, since it is automatically
# displayed by Tkinter.

root.config(menu=menubar)

root.mainloop()
