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
    # 
    # attach_next_to(child, sibling, side, width, height)
    #   child (Gtk.Widget) – the widget to add
    #   sibling (Gtk.Widget or None) – the child of grid that child will be placed next to, or None to place child at the beginning or end
    #   side (Gtk.PositionType) – the side of sibling that child is positioned next to
    #   width (int) – the number of columns that child will span
    #   height (int) – the number of rows that child will span
    # SEE: http://lazka.github.io/pgi-docs/Gtk-3.0/classes/Grid.html#Gtk.Grid.attach_next_to
    grid.add(button1)
    grid.attach(button2, left=1, top=0, width=2, height=1)
    grid.attach_next_to(button3, sibling=button1, side=gtk.PositionType.BOTTOM, width=1, height=2)
    grid.attach_next_to(button4, sibling=button3, side=gtk.PositionType.RIGHT, width=2, height=1)
    grid.attach(button5, left=1, top=2, width=1, height=1)
    grid.attach_next_to(button6, sibling=button5, side=gtk.PositionType.RIGHT, width=1, height=1)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

