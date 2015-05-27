#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/layout.html
     http://learngtk.org/tutorials/python_gtk3_tutorial/html/notebook.html
"""

from gi.repository import Gtk as gtk

def main():
    window = gtk.Window()

    notebook = gtk.Notebook()
    window.add(notebook)

    button1 = gtk.Button(label="Button 1")
    label1 = gtk.Label(label="Btn 1")
    notebook.append_page(button1, label1)

    button2 = gtk.Button(label="Button 2")
    label2 = gtk.Label(label="Btn 2")
    notebook.append_page(button2, label2)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

