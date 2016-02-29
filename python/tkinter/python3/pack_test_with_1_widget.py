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


def main():
    """Main function"""

    # WINDOW 1 (there should be only one "Tk" object) #########################

    window1 = tk.Tk()
    window1.title("Result Window")

    frame1 = tk.Frame(window1, bg="red", width=200, height=200)
    frame1.pack()

    frame1_pack_info = frame1.pack_info()


    # WINDOW 2 (Toplevel object) ##############################################

    window2 = tk.Toplevel()
    window2.title("Control Window")
    window2.geometry("+200+200")

    # Fill frame
    frame_fill = tk.LabelFrame(window2, text="Fill", padx=5, pady=5)
    frame_fill.pack(fill=tk.X, padx=10, pady=5)

    var_fill = tk.StringVar()
    var_fill.set(frame1_pack_info['fill'])

    def fill_callback():
        frame1.pack_configure(fill=var_fill.get())
        print(frame1.pack_info())

    rb_fill_none = tk.Radiobutton(frame_fill, text="NONE", variable=var_fill, value="none", command=fill_callback)
    rb_fill_x =    tk.Radiobutton(frame_fill, text="X",    variable=var_fill, value="x",    command=fill_callback)
    rb_fill_y =    tk.Radiobutton(frame_fill, text="Y",    variable=var_fill, value="y",    command=fill_callback)
    rb_fill_both = tk.Radiobutton(frame_fill, text="BOTH", variable=var_fill, value="both", command=fill_callback)

    rb_fill_none.pack(anchor=tk.W)
    rb_fill_x.pack(anchor=tk.W)
    rb_fill_y.pack(anchor=tk.W)
    rb_fill_both.pack(anchor=tk.W)

    # Expand frame
    frame_expand = tk.LabelFrame(window2, text="Expand", padx=5, pady=5)
    frame_expand.pack(fill=tk.X, padx=10, pady=5)

    var_expand = tk.IntVar()
    var_expand.set(frame1_pack_info['expand'])

    def expand_callback():
        print(var_expand.get())
        frame1.pack_configure(expand=var_expand.get())
        print(frame1.pack_info())

    cb_expand = tk.Checkbutton(frame_expand, text="Expand", variable=var_expand, command=expand_callback)
    cb_expand.pack(anchor=tk.W)

    # Quit button
    quit_button = tk.Button(window2, width=12, text="Quit", command=window1.quit)
    quit_button.pack()


    # MAIN LOOP ("Tk" object) #################################################
    window1.mainloop()


if __name__ == '__main__':
    main()
