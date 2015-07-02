#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is a simple Python GTK+3 TreeView CellRenderText snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/cellrenderers.html#cellrenderertext
"""

from gi.repository import Gtk as gtk
from gi.repository import Pango as pango

# Countries
DATA_LIST = [("China",         1370130000, "Asia"),
             ("India",         1271980000, "Asia"),
             ("United States", 321107000,  "North America"),
             ("Indonesia",     255461700,  "Asia"),
             ("Brazil",        204388000,  "South America"),
             ("Pakistan",      189936000,  "Asia"),
             ("Nigeria",       183523000,  "Africa"),
             ("Bangladesh",    158425000,  "Asia"),
             ("Russia",        146267288,  "Eurasia"),
             ("Japan",         126880000,  "Asia")]


def text_edited_cb(widget, path, text):
    #liststore[path][1] = text
    print(path, text)


def main():
    window = gtk.Window()
    window.set_default_size(300, 450)
    window.set_border_width(18)

    # Creating the ListStore model
    liststore = gtk.ListStore(str, int, str)
    for item in DATA_LIST:
        liststore.append(list(item))

    # Creating the treeview and add the columns
    treeview = gtk.TreeView(liststore)

    for column_index, column_title in enumerate(["Country", "Population", "Continent"]):
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn(column_title, renderer, text=column_index)

        # "Population" is editable
        if column_title in ("Population"):
            renderer.set_property("editable", True)
            renderer.connect("edited", text_edited_cb)

        treeview.append_column(column)

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

