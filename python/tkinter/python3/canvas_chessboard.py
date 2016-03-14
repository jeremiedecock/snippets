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

# See: http://effbot.org/tkinterbook/canvas.htm

import tkinter as tk

SQUARE_SIZE = 30  # pixels
SQUARE_NUM = 8    # squares per side

root = tk.Tk()

canvas = tk.Canvas(root,
                   width=SQUARE_NUM*SQUARE_SIZE,
                   height=SQUARE_NUM*SQUARE_SIZE)
canvas.pack(padx=10, pady=10)

for row_index in range(SQUARE_NUM):
    for col_index in range(SQUARE_NUM):
        color = "white" if (row_index + col_index) % 2 == 0 else "black"
        tags = ("square", "{}x{}".format(col_index, row_index))

        canvas.create_rectangle(SQUARE_SIZE * col_index,       # x1
                                SQUARE_SIZE * row_index,       # y1
                                SQUARE_SIZE * (col_index + 1), # x2
                                SQUARE_SIZE * (row_index + 1), # y2
                                tag=tags,
                                fill=color,
                                activefill="firebrick3",
                                #activeoutline="firebrick1", # does not work if "width=0"
                                #activewidth=4,              # does not work if "width=0"
                                width=0)

# Bind items ##################################################################

def callback(event):               # event is a tkinter.Event object
    id_tuple = canvas.find_withtag("current")  # get the item which is under the mouse cursor

    if len(id_tuple) > 0:
        item_id = id_tuple[0]

        #print(canvas.gettags(item_id))
        item_tag1, item_tag2, item_tag3 = canvas.gettags(item_id)

        print("You have clicked on the square {} (item #{})".format(item_tag2, item_id))
        print([int(coord) for coord in item_tag2.split("x")])
    else:
        raise Exception("Unexpected error")

canvas.tag_bind("square",          # a tag string or an item id
                "<Button-1>",      # the event descriptor
                callback,          # the callback function
                add="+")           # "+" to add this binding to the previous one(s) (i.e. keep the previous binding(s)) or None to replace it or them

# Main loop ###################################################################

root.mainloop()
