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

root = tk.Tk()

label = tk.Label(root, text="Press some keys", width=50, height=10)
label.pack()

# SETUP KEYBOARD EVENT CALLBACKS

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
    elif event.keysym == "space":
        print("keypress: <space>")
    elif event.keysym == "Control_R":
        print("keypress: <Control_R>")
    elif event.keysym == "Control_L":
        print("keypress: <Control_L>")
    elif event.keysym == "Shift_R":
        print("keypress: <Shift_R>")
    elif event.keysym == "Shift_L":
        print("keypress: <Shift_L>")
    elif event.keysym == "Tab":
        print("keypress: <Tab>")
    elif event.keysym == "Super_R":
        print("keypress: <Super_R>")
    elif event.keysym == "Super_L":
        print("keypress: <Super_L>")
    elif event.keysym == "BackSpace":
        print("keypress: <BackSpace>")
    elif event.keysym == "Prior":    # PgUp
        print("keypress: <Prior>")
    elif event.keysym == "Next":     # PgDown
        print("keypress: <Next>")
    elif event.char == "a":
        print("keypress: <a>")
    elif event.char == "b":
        print("keypress: <b>")
    elif event.char == "c":
        print("keypress: <c>")
    elif event.char == "d":
        print("keypress: <d>")
    elif event.char == "A":
        print("keypress: <A>")
    elif event.char == "B":
        print("keypress: <B>")
    elif event.char == "C":
        print("keypress: <C>")
    elif event.char == "D":
        print("keypress: <D>")
    elif event.char == "1":
        print("keypress: <1>")
    elif event.char == "2":
        print("keypress: <2>")
    elif event.char == "3":
        print("keypress: <3>")
    else:
        print("keypress:", event.char, event.keysym)

def keyrelease_callback(event):
    if event.keysym == "Up":
        print("keyrelease: <Up>")
    elif event.keysym == "Down":
        print("keyrelease: <Down>")
    elif event.keysym == "Left":
        print("keyrelease: <Left>")
    elif event.keysym == "Right":
        print("keyrelease: <Right>")
    elif event.keysym == "Return":
        print("keyrelease: <Return>")
    elif event.keysym == "Escape":
        print("keyrelease: <Escape>")
    elif event.keysym == "space":
        print("keyrelease: <space>")
    elif event.keysym == "Control_R":
        print("keyrelease: <Control_R>")
    elif event.keysym == "Control_L":
        print("keyrelease: <Control_L>")
    elif event.keysym == "Shift_R":
        print("keyrelease: <Shift_R>")
    elif event.keysym == "Shift_L":
        print("keyrelease: <Shift_L>")
    elif event.keysym == "Tab":
        print("keyrelease: <Tab>")
    elif event.keysym == "Super_R":
        print("keyrelease: <Super_R>")
    elif event.keysym == "Super_L":
        print("keyrelease: <Super_L>")
    elif event.keysym == "BackSpace":
        print("keyrelease: <BackSpace>")
    elif event.keysym == "Prior":    # PgUp
        print("keyrelease: <Prior>")
    elif event.keysym == "Next":     # PgDown
        print("keyrelease: <Next>")
    elif event.char == "a":
        print("keyrelease: <a>")
    elif event.char == "b":
        print("keyrelease: <b>")
    elif event.char == "c":
        print("keyrelease: <c>")
    elif event.char == "d":
        print("keyrelease: <d>")
    elif event.char == "A":
        print("keyrelease: <A>")
    elif event.char == "B":
        print("keyrelease: <B>")
    elif event.char == "C":
        print("keyrelease: <C>")
    elif event.char == "D":
        print("keyrelease: <D>")
    elif event.char == "1":
        print("keyrelease: <1>")
    elif event.char == "2":
        print("keyrelease: <2>")
    elif event.char == "3":
        print("keyrelease: <3>")
    else:
        print("keyrelease:", event.char, event.keysym)

root.bind("<KeyPress>", keypress_callback)
root.bind("<KeyRelease>", keyrelease_callback)

root.mainloop()
