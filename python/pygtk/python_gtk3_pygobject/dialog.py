#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 dialog snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/dialogs.html
"""

from gi.repository import Gtk as gtk

def on_info_clicked(widget, data):
    dialog = gtk.MessageDialog(parent=data, flags=0, message_type=gtk.MessageType.INFO, buttons=gtk.ButtonsType.OK, message_format="This is an INFO MessageDialog")
    dialog.format_secondary_text("And this is the secondary text that explains things.")
    dialog.run()
    print("INFO dialog closed")
    dialog.destroy()

def on_error_clicked(widget, data):
    dialog = gtk.MessageDialog(parent=data, flags=0, message_type=gtk.MessageType.ERROR, buttons=gtk.ButtonsType.CANCEL, message_format="This is an ERROR MessageDialog")
    dialog.format_secondary_text("And this is the secondary text that explains things.")
    dialog.run()
    print("ERROR dialog closed")
    dialog.destroy()

def on_warn_clicked(widget, data):
    dialog = gtk.MessageDialog(parent=data, flags=0, message_type=gtk.MessageType.WARNING, buttons=gtk.ButtonsType.OK_CANCEL, message_format="This is an WARNING MessageDialog")
    dialog.format_secondary_text( "And this is the secondary text that explains things.")
    response = dialog.run()
    if response == gtk.ResponseType.OK:
        print("WARN dialog closed by clicking OK button")
    elif response == gtk.ResponseType.CANCEL:
        print("WARN dialog closed by clicking CANCEL button")
    dialog.destroy()

def on_question_clicked(widget, data):
    dialog = gtk.MessageDialog(parent=data, flags=0, message_type=gtk.MessageType.QUESTION, buttons=gtk.ButtonsType.YES_NO, message_format="This is an QUESTION MessageDialog")
    dialog.format_secondary_text( "And this is the secondary text that explains things.")
    response = dialog.run()
    if response == gtk.ResponseType.YES:
        print("QUESTION dialog closed by clicking YES button")
    elif response == gtk.ResponseType.NO:
        print("QUESTION dialog closed by clicking NO button")
    dialog.destroy()

def main():
    window = gtk.Window(title="GtkMessageDialog snippet")
    window.set_border_width(10)

    # Box
    box = gtk.Box(orientation = gtk.Orientation.VERTICAL, spacing=6)
    window.add(box)

    # Buttons
    button1 = gtk.Button("Information")
    button1.connect("clicked", on_info_clicked, window)
    box.add(button1)

    button2 = gtk.Button("Error")
    button2.connect("clicked", on_error_clicked, window)
    box.add(button2)

    button3 = gtk.Button("Warning")
    button3.connect("clicked", on_warn_clicked, window)
    box.add(button3)

    button4 = gtk.Button("Question")
    button4.connect("clicked", on_question_clicked, window)
    box.add(button4)

    # Run
    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

