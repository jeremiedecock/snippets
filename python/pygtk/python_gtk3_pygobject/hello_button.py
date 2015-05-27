#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/introduction.html
"""

from gi.repository import Gtk as gtk

def on_button_clicked(widget):
    print("Hello World!")

def main():
    window = gtk.Window()

    button = gtk.Button(label="Click Here")
    button.connect("clicked", on_button_clicked)
    window.add(button)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

