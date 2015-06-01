#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/textview.html
"""

from gi.repository import Gtk as gtk

def print_text(widget, data):
    """
    Print the content of the TextView widget.

    This is an usage example fo gtk.TextView.get_buffer().get_text().
    """
    text_buffer = data.get_buffer()    # data is a gtk.TextView widget
    text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter(), True)
    print(text)

def clear_text(widget, data):
    """
    Clear the content of the TextView widget.

    This is an usage example fo gtk.TextView.get_buffer().set_text().
    """
    data.get_buffer().set_text("")     # data is a gtk.TextView widget

def main():
    window = gtk.Window()
    window.set_default_size(300, 450)

    vertical_box = gtk.Box(orientation = gtk.Orientation.VERTICAL, spacing=6)       # number of pixels placed between children
    vertical_box.set_border_width(18)

    window.add(vertical_box)

    # Label ###########################

    label = gtk.Label(label="Text to print:")
    label.set_alignment(0, 0.5)                                                     # Align left

    vertical_box.pack_start(label, expand=False, fill=True, padding=0)

    # TextView ########################

    textview = gtk.TextView()
    textview.set_wrap_mode(gtk.WrapMode.WORD)                                       # wrap the text, if needed, breaking lines in between words

    scrolled_window = gtk.ScrolledWindow()
    scrolled_window.set_border_width(0)
    scrolled_window.set_shadow_type(gtk.ShadowType.IN)                              # should be gtk.ShadowType.IN, gtk.ShadowType.OUT, gtk.ShadowType.ETCHED_IN or gtk.ShadowType.ETCHED_OUT
    scrolled_window.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS)     # should be gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS or gtk.PolicyType.NEVER
    scrolled_window.add(textview)

    vertical_box.pack_start(scrolled_window, expand=True, fill=True, padding=0)

    # Buttons #########################

    horizontal_box = gtk.Box(orientation = gtk.Orientation.HORIZONTAL, spacing=12)   # number of pixels placed between children

    # Print button
    button1 = gtk.Button(label="Print")
    button1.connect("clicked", print_text, textview)  # connect("event", callback, data)
    horizontal_box.pack_start(button1, expand=True, fill=True, padding=0)

    # Clean button
    button2 = gtk.Button(label="Clear")
    button2.connect("clicked", clear_text, textview)  # connect("event", callback, data)
    horizontal_box.pack_start(button2, expand=True, fill=True, padding=0)

    vertical_box.pack_start(horizontal_box, expand=False, fill=True, padding=0)

    ###

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

