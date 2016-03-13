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

# See: http://effbot.org/tkinterbook/frame.htm

import tkinter as tk

# WINDOW 1 (there should be only one "Tk" object) #########################

window1 = tk.Tk()
window1.title("Result Window")

widget1 = tk.Canvas(window1, bg="red", width=200, height=200)
widget1.create_text((100, 100), text="Widget 1", font="sans 16 bold", fill="white", anchor="c")
widget1.pack()

frame1_pack_info = widget1.pack_info()

# WINDOW 2 (Toplevel object) ##############################################

window2 = tk.Toplevel()
window2.title("Control Window")
window2.geometry("+200+200")

# Widget 1 frame ##################

frame_widget1 = tk.LabelFrame(window2, text="Widget 1", padx=5, pady=5)
frame_widget1.pack(fill=tk.X, padx=10, pady=5)

# Fill ########

# Must be none, x, y, or both

var_fill = tk.StringVar()
var_fill.set(frame1_pack_info['fill'])

def fill_callback():
    widget1.pack_configure(fill=var_fill.get())
    print("Widget 1:", widget1.pack_info())

rb_fill_none = tk.Radiobutton(frame_widget1, text="fill = none", variable=var_fill, value="none", command=fill_callback)
rb_fill_x =    tk.Radiobutton(frame_widget1, text="fill = x",    variable=var_fill, value="x",    command=fill_callback)
rb_fill_y =    tk.Radiobutton(frame_widget1, text="fill = y",    variable=var_fill, value="y",    command=fill_callback)
rb_fill_both = tk.Radiobutton(frame_widget1, text="fill = both", variable=var_fill, value="both", command=fill_callback)

rb_fill_none.pack(anchor=tk.W)
rb_fill_x.pack(anchor=tk.W)
rb_fill_y.pack(anchor=tk.W)
rb_fill_both.pack(anchor=tk.W)

# Separator
tk.Frame(frame_widget1, height=1, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

# Expand ######

var_expand = tk.IntVar()
var_expand.set(frame1_pack_info['expand'])

def expand_callback():
    print(var_expand.get())
    widget1.pack_configure(expand=var_expand.get())
    print("Widget 1:", widget1.pack_info())

cb_expand = tk.Checkbutton(frame_widget1, text="expand", variable=var_expand, command=expand_callback)
cb_expand.pack(anchor=tk.W)

# Separator
tk.Frame(frame_widget1, height=1, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

# Side ########

# Must be top, bottom, left, or right

var_side = tk.StringVar()
var_side.set(frame1_pack_info['side'])

def side_callback():
    widget1.pack_configure(side=var_side.get())
    print("Widget 1:", widget1.pack_info())

rb_side_top =    tk.Radiobutton(frame_widget1, text="side = top",    variable=var_side, value="top",    command=side_callback)
rb_side_bottom = tk.Radiobutton(frame_widget1, text="side = bottom", variable=var_side, value="bottom", command=side_callback)
rb_side_left =   tk.Radiobutton(frame_widget1, text="side = left",   variable=var_side, value="left",   command=side_callback)
rb_side_right =  tk.Radiobutton(frame_widget1, text="side = right",  variable=var_side, value="right",  command=side_callback)

rb_side_top.pack(anchor=tk.W)
rb_side_bottom.pack(anchor=tk.W)
rb_side_left.pack(anchor=tk.W)
rb_side_right.pack(anchor=tk.W)

# Separator
tk.Frame(frame_widget1, height=1, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

# Anchor ######

# Must be n, ne, e, se, s, sw, w, nw, or center

var_anchor = tk.StringVar()
var_anchor.set(frame1_pack_info['anchor'])

def anchor_callback():
    widget1.pack_configure(anchor=var_anchor.get())
    print("Widget 1:", widget1.pack_info())

rb_anchor_n      = tk.Radiobutton(frame_widget1, text="anchor = n",      variable=var_anchor, value="n",      command=anchor_callback)
rb_anchor_s      = tk.Radiobutton(frame_widget1, text="anchor = s",      variable=var_anchor, value="s",      command=anchor_callback)
rb_anchor_e      = tk.Radiobutton(frame_widget1, text="anchor = e",      variable=var_anchor, value="e",      command=anchor_callback)
rb_anchor_w      = tk.Radiobutton(frame_widget1, text="anchor = w",      variable=var_anchor, value="w",      command=anchor_callback)
rb_anchor_ne     = tk.Radiobutton(frame_widget1, text="anchor = ne",     variable=var_anchor, value="ne",     command=anchor_callback)
rb_anchor_nw     = tk.Radiobutton(frame_widget1, text="anchor = nw",     variable=var_anchor, value="nw",     command=anchor_callback)
rb_anchor_se     = tk.Radiobutton(frame_widget1, text="anchor = se",     variable=var_anchor, value="se",     command=anchor_callback)
rb_anchor_sw     = tk.Radiobutton(frame_widget1, text="anchor = sw",     variable=var_anchor, value="sw",     command=anchor_callback)
rb_anchor_center = tk.Radiobutton(frame_widget1, text="anchor = center", variable=var_anchor, value="center", command=anchor_callback)

rb_anchor_n.pack(anchor=tk.W)
rb_anchor_s.pack(anchor=tk.W)
rb_anchor_e.pack(anchor=tk.W)
rb_anchor_w.pack(anchor=tk.W)
rb_anchor_ne.pack(anchor=tk.W)
rb_anchor_nw.pack(anchor=tk.W)
rb_anchor_se.pack(anchor=tk.W)
rb_anchor_sw.pack(anchor=tk.W)
rb_anchor_center.pack(anchor=tk.W)

# Setup close button ##############

# Let window2's close button quit the application
window2.protocol("WM_DELETE_WINDOW", window1.quit)

# MAIN LOOP ("Tk" object) #################################################

window1.mainloop()
