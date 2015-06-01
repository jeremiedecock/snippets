#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/layout.html

"Gtk.Grid is a container which arranges its child widgets in rows and columns,
but you do not need to specify the dimensions in the constructor. Children are
added using Gtk.Grid.attach(). They can span multiple rows or columns. It is
also possible to add a child next to an existing child, using
Gtk.Grid.attach_next_to().
Gtk.Grid can be used like a Gtk.Box by just using Gtk.Grid.add(), which will
place children next to each other in the direction determined by the
“orientation” property (defaults to Gtk.Orientation.HORIZONTAL)."
"""

from gi.repository import Gtk as gtk

def main():
    window = gtk.Window()

    grid = gtk.Grid()
    grid.set_column_homogeneous(True)
    grid.set_column_spacing(3)
    grid.set_row_homogeneous(False)
    grid.set_row_spacing(3)

    window.add(grid)

    button1 = gtk.Button(label="Btn 1")
    button2 = gtk.Button(label="Btn 2")
    button3 = gtk.Button(label="Btn 3")
    button4 = gtk.Button(label="Btn 4")
    button5 = gtk.Button(label="Btn 5")
    button6 = gtk.Button(label="Btn 6")

    # grid.attach(child, left, top, width, height)
    #   child (Gtk.Widget) – the widget to add
    #   left (int) – the column number to attach the left side of child to
    #   top (int) – the row number to attach the top side of child to
    #   width (int) – the number of columns that child will span
    #   height (int) – the number of rows that child will span
    # SEE: http://lazka.github.io/pgi-docs/Gtk-3.0/classes/Grid.html#Gtk.Grid.attach
    grid.attach(button1, left=0, top=0, width=1, height=1)
    grid.attach(button2, left=1, top=0, width=2, height=1)
    grid.attach(button3, left=0, top=1, width=1, height=2)
    grid.attach(button4, left=1, top=1, width=2, height=1)
    grid.attach(button5, left=1, top=2, width=1, height=1)
    grid.attach(button6, left=2, top=2, width=1, height=1)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

