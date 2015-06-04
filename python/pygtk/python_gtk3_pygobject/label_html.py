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

    label = gtk.Label()
    label.set_markup('Text can be <small>small</small>, <big>big</big>, <b>bold</b>, <i>italic</i> and even point to somewhere <a href="http://www.jdhp.org">www.jdhp.org</a>.')
    window.add(label)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

