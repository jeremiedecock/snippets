#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/button_widgets.html#checkbutton
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

    hbox = gtk.Box(spacing=6)
    window.add(hbox)

    button1 = gtk.CheckButton(label="Button 1")
    button1.connect("toggled", on_button_toggled)
    hbox.pack_start(button1, expand=True, fill=True, padding=0)

    button2 = gtk.CheckButton(label="Button 2")
    button2.set_active(True)
    button2.connect("toggled", on_button_toggled)
    hbox.pack_start(button2, expand=True, fill=True, padding=0)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

