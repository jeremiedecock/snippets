#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/layout.html
"""

from gi.repository import Gtk as gtk

def main():
    window = gtk.Window()

    vertical_box = gtk.Box(orientation = gtk.Orientation.VERTICAL, spacing=6)       # 6 pixels are placed between children
    horizontal_box = gtk.Box(orientation = gtk.Orientation.HORIZONTAL, spacing=6)   # 6 pixels are placed between children

    window.add(vertical_box)

    ###

    button1 = gtk.Button(label="Btn 1")
    vertical_box.pack_start(button1, expand=True, fill=True, padding=0)

    vertical_box.pack_start(horizontal_box, expand=True, fill=True, padding=0)

    ###

    button2 = gtk.Button(label="Btn 2")
    horizontal_box.pack_start(button2, expand=True, fill=True, padding=0)

    button3 = gtk.Button(label="Btn 3")
    horizontal_box.pack_start(button3, expand=True, fill=True, padding=0)

    ###

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

