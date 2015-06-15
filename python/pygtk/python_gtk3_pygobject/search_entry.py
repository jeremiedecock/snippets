#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
A simple Python GTK+3 SearchEntry snippet.

API: http://lazka.github.io/pgi-docs/Gtk-3.0/classes/SearchEntry.html
"""

from gi.repository import Gtk as gtk

def print_text(widget, data):
    """
    Print the content of the Entry widget.

    This is an usage example fo gtk.Entry.get_text().
    """
    entry = data       # data is a gtk.Entry widget

    print(entry.get_text())


def clear_text(widget, data):
    """
    Clear the content of the Entry widget.

    This is an usage example fo gtk.Entry.set_text().
    """
    entry = data       # data is a gtk.Entry widget

    entry.set_text("")


def main():
    window = gtk.Window()
    window.set_border_width(10)

    # Label and Entry #################

    # Label
    label = gtk.Label(label="Text to print:")
    label.set_alignment(0, 0.5)               # Align left

    # Entry
    entry = gtk.SearchEntry()

    # Buttons #########################

    # Print button
    button1 = gtk.Button(label="Print")
    button1.connect("clicked", print_text, entry)  # connect("event", callback, data)

    # Clean button
    button2 = gtk.Button(label="Clear")
    button2.connect("clicked", clear_text, entry)  # connect("event", callback, data)

    # Box containers ##################

    horizontal_box1 = gtk.Box(orientation = gtk.Orientation.HORIZONTAL, spacing=6)   # 6 pixels are placed between children
    horizontal_box1.pack_start(label, expand=True, fill=True, padding=0)
    horizontal_box1.pack_start(entry, expand=True, fill=True, padding=0)

    horizontal_box2 = gtk.Box(orientation = gtk.Orientation.HORIZONTAL, spacing=6)   # 6 pixels are placed between children
    horizontal_box2.pack_start(button1, expand=True, fill=True, padding=0)
    horizontal_box2.pack_start(button2, expand=True, fill=True, padding=0)

    vertical_box = gtk.Box(orientation = gtk.Orientation.VERTICAL, spacing=6)       # 6 pixels are placed between children
    vertical_box.pack_start(horizontal_box1, expand=True, fill=True, padding=0)
    vertical_box.pack_start(horizontal_box2, expand=True, fill=True, padding=0)

    window.add(vertical_box)

    ###

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

