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


# WARNING!
# The following commented version would NOT work properly because of the Python scopes:
#
#     for label in ["Banana", "Apple", "Mango"]:
#         button = tk.Button(root,
#                            text=label,
#                            command=lambda: callback(label))
#         button.pack()
#
# Indeed, the value of the "label" variable given in the lambda function is a
# reference not a copy; thus here, all buttons would print "Mango"!
#
# A copy of "label" should be given to the lambda function like in the
# following version ("arg" is a copy of "label", not a reference).
#
# See the following links for more information:
# - http://effbot.org/zone/tkinter-callbacks.htm
# - http://stackoverflow.com/questions/728356/dynamically-creating-a-menu-in-tkinter-lambda-expressions
# - http://stackoverflow.com/questions/938429/scope-of-python-lambda-functions-and-their-parameters
# - http://stackoverflow.com/questions/19693782/callback-function-tkinter-button-with-variable-parameter

import tkinter as tk

def callback(arg):
    """A callback with an argument."""
    print(arg)

root = tk.Tk()

for label in ["Banana", "Apple", "Mango"]:
    button = tk.Button(root,
                       text=label,
                       command=lambda arg=label: callback(arg))
    button.pack()

root.mainloop()

