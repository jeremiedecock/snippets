#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: https://developer.gnome.org/gnome-devel-demos/stable/image.py.html.en
"""

from gi.repository import Gtk as gtk

def main():
    window = gtk.Window()

    # create an image
    image = gtk.Image()

    # set the content of the image as the file filename.png
    image.set_from_file("image.png")

    # add the image to the window
    window.add(image)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

