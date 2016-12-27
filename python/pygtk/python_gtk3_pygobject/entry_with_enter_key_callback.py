#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
A simple Python GTK+3 Entry snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/entry.html

API: http://lazka.github.io/pgi-docs/Gtk-3.0/classes/Entry.html
"""

from gi.repository import Gtk as gtk

def print_text(widget, data):
    """
    Print the content of the Entry widget.

    This is an usage example fo gtk.Entry.get_text().
    """
    entry = data       # data is a gtk.Entry widget
    print(entry.get_text())


def main():
    window = gtk.Window()
    window.set_border_width(10)

    # Entry ###########################

    print("Type a text in the entry and press enter to print it in the terminal")

    # Entry
    entry = gtk.Entry()
    entry.connect("activate", print_text, entry)  # <<< call "print_text()" function when the "Enter" key is pressed in the entry
                                                  # connect("event", callback, data)

    # Box container ###################

    box = gtk.Box(orientation = gtk.Orientation.VERTICAL, spacing=6)   # 6 pixels are placed between children
    box.pack_start(entry, expand=True, fill=True, padding=0)

    window.add(box)

    ###

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

