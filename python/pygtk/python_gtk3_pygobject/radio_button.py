#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/button_widgets.html#radiobutton
"""

from gi.repository import Gtk as gtk

def on_button_toggled(widget):
    if widget.get_active():
        print(widget.get_label(), " was turned ON")
    else:
        print(widget.get_label(), " was turned OFF")

def main():
    window = gtk.Window()
    window.set_border_width(10)

    grid = gtk.Grid()
    window.add(grid)

    button1 = gtk.RadioButton(label="Button 1 (group 1)")
    button1.connect("toggled", on_button_toggled)

    button2 = gtk.RadioButton(label="Button 2 (group 1)")
    button2.connect("toggled", on_button_toggled)

    button3 = gtk.RadioButton(label="Button 3 (group 1)")
    button3.connect("toggled", on_button_toggled)

    button4 = gtk.RadioButton(label="Button 4 (group 2)")
    button4.connect("toggled", on_button_toggled)

    button5 = gtk.RadioButton(label="Button 5 (group 2)")
    button5.connect("toggled", on_button_toggled)

    button2.join_group(button1)
    button3.join_group(button1)
    button5.join_group(button4)

    button3.set_active(True)

    grid.attach(button1, left=0, top=0, width=1, height=1)
    grid.attach(button2, left=1, top=0, width=1, height=1)
    grid.attach(button3, left=2, top=0, width=1, height=1)
    grid.attach(button4, left=0, top=1, width=1, height=1)
    grid.attach(button5, left=1, top=1, width=1, height=1)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

