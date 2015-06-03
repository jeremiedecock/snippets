#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 Paned snippet.

See: https://lazka.github.io/pgi-docs/Gtk-3.0/classes/Paned.html
     http://learngtk.org/tutorials/python_gtk3_tutorial/html/paned.html
"""

from gi.repository import Gtk as gtk

def main():
    window = gtk.Window()

    paned = gtk.Paned(orientation=gtk.Orientation.VERTICAL) # gtk.Orientation.HORIZONTAL or gtk.Orientation.VERTICAL
    paned.set_position(30)                                  # Sets the position in pixels of the divider between the two panes (i.e. the default size of the first pane)
    window.add(paned)

    button1 = gtk.Button(label="Btn 1")
    paned.add1(button1)
    #paned.add1(button1, resize=True, shrink=True)

    button2 = gtk.Button(label="Btn 2")
    paned.add2(button2)
    #paned.add2(button2, resize=True, shrink=True)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

