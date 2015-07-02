#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is a simple Python GTK+3 TreeView CellRenderText snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/cellrenderers.html#cellrenderertoggle
"""

from gi.repository import Gtk as gtk

MANUFACTURERS = ["Sony", "LG", "Panasonic", "Toshiba", "Nokia", "Samsung"]

HARDWARE = [("Television",   "Samsung"),
            ("Mobile Phone", "LG"),
            ("DVD Player",   "Panasonic")]

def main():
    window = gtk.Window()
    window.set_default_size(300, 450)
    window.set_border_width(18)

    # Creating the manufacturers ListStore model
    liststore_manufacturers = gtk.ListStore(str)
    for item in MANUFACTURERS:
        liststore_manufacturers.append([item])

    # Creating the hardware ListStore model
    liststore_hardware = gtk.ListStore(str, str)
    for item in HARDWARE:
        liststore_hardware.append(list(item))

    # Creating the treeview and add the columns
    treeview = gtk.TreeView(model=liststore_hardware)

    # Text column
    renderer1 = gtk.CellRendererText()
    column1_title = "Text"
    column1_index = 0
    column1 = gtk.TreeViewColumn(column1_title, renderer1, text=column1_index)
    treeview.append_column(column1)

    # Combo column
    renderer2 = gtk.CellRendererCombo()
    column2_title = "Combo"
    column2_index = 1
    column2 = gtk.TreeViewColumn(column2_title, renderer2, text=column2_index)
    treeview.append_column(column2)

    renderer2.set_property("editable", True)
    renderer2.set_property("model", liststore_manufacturers)
    renderer2.set_property("text-column", 0)
    renderer2.set_property("has-entry", False)

    def on_combo_changed_cb(widget, path, text):
        liststore_hardware[path][1] = text

    renderer2.connect("edited", on_combo_changed_cb)

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

