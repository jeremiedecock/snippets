#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is a simple Python GTK+3 TreeView sort snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/treeview.html
"""

from gi.repository import Gtk as gtk

# Countries, population (as in 2015) and continent.
DATA_LIST = [("China", 1370130000, "Asia"),
             ("India", 1271980000, "Asia"),
             ("United States", 321107000, "America"),
             ("Indonesia", 255461700, "Asia"),
             ("Brazil", 204388000, "America"),
             ("Pakistan", 189936000, "Asia"),
             ("Nigeria", 183523000, "Africa"),
             ("Bangladesh", 158425000, "Asia"),
             ("Russia", 146267288, "Eurasia"),
             ("Japan", 126880000, "Asia")]

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

        # Note that the column_id given to set_sort_column_id() refers to the
        # column of the model and not to the TreeView’s column.
        # When the user clic on the header of the TreeView’s column
        # (corresponding to the current "column" variable), the TreeView is
        # sorted according to the model's data in the column indexed by
        # "column_id".
        # Here, we simply use "column_id" = "column_index" because the TreeView
        # displays all columns of the model (in the same order) ; but in some
        # other cases, this may be wrong and the following commented code should
        # be used:
        #
        #   if column_title == "Country":
        #       column.set_sort_column_id(0)   # sort according to the first model's column
        #   elif column_title == "Population":
        #       column.set_sort_column_id(1)   # sort according to the second model's column
        #   elif column_title == "Continent":
        #       column.set_sort_column_id(2)   # sort according to the third model's column
        #
        column.set_sort_column_id(column_index)


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

