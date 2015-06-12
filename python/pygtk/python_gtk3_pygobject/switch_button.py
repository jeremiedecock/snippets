#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 SwitchButton snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/button_widgets.html#togglebutton
"""

from gi.repository import Gtk as gtk

def on_switch_activated(widget, param):
    if widget.get_active():
        print("The switch was turned ON")
    else:
        print("The switch was turned OFF")

def main():
    window = gtk.Window()
    window.set_border_width(10)

    button = gtk.Switch()
    button.connect("notify::active", on_switch_activated)
    button.set_active(False)

    window.add(button)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

