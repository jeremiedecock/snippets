#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is a simple Python GTK+3 TreeView CellRenderText snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/cellrenderers.html#cellrenderertoggle
"""

from gi.repository import Gtk as gtk
from gi.repository import Pango as pango

# Countries
DATA_LIST = [("China",         True,  True),
             ("India",         False, False),
             ("United States", False, False),
             ("Indonesia",     False, False),
             ("Brazil",        False, False),
             ("Pakistan",      False, False),
             ("Nigeria",       False, False),
             ("Bangladesh",    False, False),
             ("Russia",        False, False),
             ("Japan",         False, False)]


def main():
    window = gtk.Window()
    window.set_default_size(300, 450)
    window.set_border_width(18)

    # Creating the ListStore model
    liststore = gtk.ListStore(str, bool, bool)
    for item in DATA_LIST:
        liststore.append(list(item))

    # Creating the treeview and add the columns
    treeview = gtk.TreeView(liststore)

    # Country column
    renderer1 = gtk.CellRendererText()
    column1_title = "Text"
    column1_index = 0
    column1 = gtk.TreeViewColumn(column1_title, renderer1, text=column1_index)
    treeview.append_column(column1)

    # Checkbox column
    renderer2 = gtk.CellRendererToggle()
    column2_title = "Checkbox"
    column2_index = 1
    column2 = gtk.TreeViewColumn(column2_title, renderer2, active=column2_index)
    treeview.append_column(column2)

    def on_cell_checkbox_toggled_cb(widget, path):
        liststore[path][1] = not liststore[path][1]

    renderer2.connect("toggled", on_cell_checkbox_toggled_cb)

    # Radio button column
    renderer3 = gtk.CellRendererToggle()
    column3_title = "Radio button"
    column3_index = 2
    column3 = gtk.TreeViewColumn(column3_title, renderer3, active=column3_index)
    treeview.append_column(column3)

    def on_cell_radio_button_toggled_cb(widget, path):
        selected_path = gtk.TreePath(path)
        for row in liststore:
            row[2] = (row.path == selected_path)

    renderer3.connect("toggled", on_cell_radio_button_toggled_cb)
    renderer3.set_radio(True)

    # Scrolled window
    scrolled_window = gtk.ScrolledWindow()
    scrolled_window.set_border_width(0)
    scrolled_window.set_shadow_type(gtk.ShadowType.IN)                              # should be gtk.ShadowType.IN, gtk.ShadowType.OUT, gtk.ShadowType.ETCHED_IN or gtk.ShadowType.ETCHED_OUT
    scrolled_window.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS)     # should be gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS or gtk.PolicyType.NEVER
    scrolled_window.add(treeview)

    window.add(scrolled_window)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

