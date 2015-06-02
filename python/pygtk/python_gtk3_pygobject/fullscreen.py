#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/label.html
"""

from gi.repository import Gtk as gtk

def main():
    window = gtk.Window()
    window.fullscreen()

    # To return to window mode, use: window.unfullscreen()

    label = gtk.Label(label="Hello!\n¡Buenos días!\nBonjour!\n你好！")
    window.add(label)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

