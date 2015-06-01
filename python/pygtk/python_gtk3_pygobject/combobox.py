#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/combobox.html

"For a simple list of textual choices, the model-view API of Gtk.ComboBox can
be a bit overwhelming. In this case, Gtk.ComboBoxText offers a simple
alternative."
"""

from gi.repository import Gtk as gtk

COMBOBOX_TEXT_LIST = ["Hello World!", "Hi!", "Goodbye."]

def print_text(widget, data):
    """
    Print the content of the ComboBoxText widget.

    This is an usage example fo gtk.ComboBoxText.get_active_text().
    """
    print(data.get_active_text())      # data is a gtk.ComboBoxText widget

def reset_selection(widget, data):
    """
    Clear the content of the ComboBoxText widget.

    This is an usage example fo gtk.ComboBoxText.set_active().
    """
    data.set_active(0)                 # select the first item ; data is a gtk.ComboBoxText widget

def main():
    window = gtk.Window()

    vertical_box = gtk.Box(orientation = gtk.Orientation.VERTICAL, spacing=6)       # 6 pixels are placed between children
    window.add(vertical_box)

    # Label and Combobox ##############

    horizontal_box1 = gtk.Box(orientation = gtk.Orientation.HORIZONTAL, spacing=6)   # 6 pixels are placed between children

    label = gtk.Label(label="Text to print:")
    label.set_alignment(0, 0.5)                                                     # Align left
    horizontal_box1.pack_start(label, expand=True, fill=True, padding=0)

    combobox = gtk.ComboBoxText()
    combobox.set_entry_text_column(0)  # sets the model column which ComboBox should use to get strings from to be text_column
    for text in COMBOBOX_TEXT_LIST:
        combobox.append_text(text)     # fill the combobox
    combobox.set_active(0)             # select the first item
    horizontal_box1.pack_start(combobox, expand=True, fill=True, padding=0)

    vertical_box.pack_start(horizontal_box1, expand=True, fill=True, padding=0)

    # Buttons #########################

    horizontal_box2 = gtk.Box(orientation = gtk.Orientation.HORIZONTAL, spacing=6)   # 6 pixels are placed between children

    # Print button
    button1 = gtk.Button(label="Print")
    button1.connect("clicked", print_text, combobox)  # connect("event", callback, data)
    horizontal_box2.pack_start(button1, expand=True, fill=True, padding=0)

    # Clean button
    button2 = gtk.Button(label="Reset")
    button2.connect("clicked", reset_selection, combobox)  # connect("event", callback, data)
    horizontal_box2.pack_start(button2, expand=True, fill=True, padding=0)

    vertical_box.pack_start(horizontal_box2, expand=True, fill=True, padding=0)

    ###

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

