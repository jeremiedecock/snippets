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

# SEE: http://effbot.org/tkinterbook/photoimage.htm#patterns

# Required Debian package (Debian 8.1 Jessie): python3-pil.imagetk

import PIL.Image as pil_img   # PIL.Image is a module not a class...
import PIL.ImageTk as pil_tk  # PIL.ImageTk is a module not a class...

import tkinter as tk
import tkinter.filedialog

if tk.TkVersion < 8.6:
    print("*" * 80)
    print("WARNING: Tk version {} is installed on your system.".format(tk.TkVersion))
    print("Tk < 8.6 only supports three file formats: GIF, PGM and PPM.")
    print("You need to install Tk >= 8.6 if you want to read JPEG and PNG images!")
    print("*" * 80)


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.opened_image_path = None

        # Create a toplevel menu
        self.menubar = tk.Menu(parent)

        # Create a pulldown menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        self.menubar.add_cascade(label="File", menu=file_menu)

        # Label
        self.label = tk.Label(parent)
        self.label.pack(fill=tk.BOTH, expand=1)

        self.label.bind('<Configure>', self.resize_callback)


    def open_file(self):
        # Here fd is a file descriptor (like "fd = open('foo', 'r')")
        fd = tk.filedialog.askopenfile()
        if fd is not None:
            self.opened_image_path = fd.name
            fd.close()

            self.load_image()


    def resize_callback(self, event):
        if self.opened_image_path is not None:
            self.update_image()


    def load_image(self):
        if self.opened_image_path is not None:
            self.pil_image = pil_img.open(self.opened_image_path)
            self.update_image()


    def update_image(self):

        # WARNING:
        # You must keep a reference to the image object in your Python program,
        # either by storing it in a global variable, or by attaching it to another
        # object!
        #
        # When a PhotoImage object is garbage-collected by Python (e.g. when you
        # return from a function which stored an image in a local variable), the
        # image is cleared even if it’s being displayed by a Tkinter widget.
        #
        # To avoid this, the program must keep an extra reference to the image
        # object. A simple way to do this is to assign the image to a widget
        # attribute, like this:
        #
        #    label = Label(image=tk_photo)
        #    label.image = tk_photo        # keep a reference!
        #    label.pack()
        #
        # (src: http://effbot.org/tkinterbook/photoimage.htm#patterns)
        # See also http://infohost.nmt.edu/tcc/help/pubs/pil/image-tk.html
        
        if self.opened_image_path is not None:
            image_width = self.pil_image.size[0]
            image_height = self.pil_image.size[1]

            widget_current_width = self.label.winfo_width()          # Current label width
            widget_current_height = self.label.winfo_height()        # Current label height
            widget_current_width = widget_current_width - 2          # TODO: fix this workaround
            widget_current_height = widget_current_height - 2        # TODO: fix this workaround

            ratio_x = widget_current_width / float(image_width)
            ratio_y = widget_current_height / float(image_height)
            ratio = min(min(ratio_x, ratio_y), 1.0)

            width = int(image_width * ratio)
            height = int(image_height * ratio)

            resized_pil_image = self.pil_image.resize((width, height), pil_img.ANTIALIAS)

            self.tk_photo = pil_tk.PhotoImage(resized_pil_image)

            self.label["image"] = self.tk_photo


def main():
    """Main function"""

    root = tk.Tk()
    root.minsize(128, 128)
    root.geometry("640x480") # Default size

    app = MainApplication(root)
    root.config(menu=app.menubar)

    root.mainloop()


if __name__ == '__main__':
    main()
