#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 LinkButton snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/introduction.html
"""

from gi.repository import Gtk as gtk

def main():
    window = gtk.Window()
    window.set_border_width(10)

    button = gtk.LinkButton(uri="http://www.jdhp.org", label="Visit www.jdhp.org")
    window.add(button)

    # TO GET THE URI: button.get_uri()
    # TO SET THE URI: button.set_uri("...")

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

