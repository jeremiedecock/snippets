#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
A simple Python GTK+3 TreeView snippet with filtering.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/treeview.html#filtering
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

current_filter_value = None

def button_clicked_cb(widget, data):
    """Called on any of the button clicks"""
    
    global current_filter_value
    button = widget
    liststore_filter = data

    # Set the current filter to the button's label
    current_filter_value = button.get_label()
    print("Show ", current_filter_value)

    # Update the filter, which updates in turn the view
    liststore_filter.refilter()

def filter_function(model, iter, data):
    """Tests if the continent in the row is the one in the filter"""
    global current_filter_value

    if current_filter_value is None or current_filter_value == "All":
        return True
    else:
        return model[iter][2] == current_filter_value

def main():
    window = gtk.Window()
    window.set_default_size(300, 450)
    window.set_border_width(18)

    # Creating the ListStore model
    liststore = gtk.ListStore(str, int, str)
    for item in DATA_LIST:
        liststore.append(list(item))

    # Setup filtering
    liststore_filter = liststore.filter_new()           # creating the filter, feeding it with the liststore model
    liststore_filter.set_visible_func(filter_function)  # setting the filter function, note that we're not using the

    # Creating the treeview and add the columns
    #treeview = gtk.TreeView(liststore) # TODO
    treeview = gtk.TreeView.new_with_model(liststore_filter)
    for column_index, column_title in enumerate(["Country", "Population", "Continent"]):
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(column_title, renderer, text=column_index)
        treeview.append_column(column)

    # Scrolled window
    scrolled_window = gtk.ScrolledWindow()
    scrolled_window.set_border_width(0)
    scrolled_window.set_shadow_type(gtk.ShadowType.IN)                              # should be gtk.ShadowType.IN, gtk.ShadowType.OUT, gtk.ShadowType.ETCHED_IN or gtk.ShadowType.ETCHED_OUT
    scrolled_window.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS)     # should be gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS or gtk.PolicyType.NEVER
    scrolled_window.add(treeview)

    # Setup the grid container
    grid = gtk.Grid()
    grid.set_column_homogeneous(True)
    grid.set_row_homogeneous(True)
    grid.set_column_spacing(3)
    grid.set_row_spacing(3)
    window.add(grid)

    # Setup buttons
    button1 = gtk.Button(label="Africa")
    button2 = gtk.Button(label="America")
    button3 = gtk.Button(label="Asia")
    button4 = gtk.Button(label="Eurasia")
    button5 = gtk.Button(label="All")

    button1.connect("clicked", button_clicked_cb, liststore_filter)
    button2.connect("clicked", button_clicked_cb, liststore_filter)
    button3.connect("clicked", button_clicked_cb, liststore_filter)
    button4.connect("clicked", button_clicked_cb, liststore_filter)
    button5.connect("clicked", button_clicked_cb, liststore_filter)

    # grid.attach(child, left, top, width, height)
    #   child (Gtk.Widget) – the widget to add
    #   left (int) – the column number to attach the left side of child to
    #   top (int) – the row number to attach the top side of child to
    #   width (int) – the number of columns that child will span
    #   height (int) – the number of rows that child will span
    # SEE: http://lazka.github.io/pgi-docs/Gtk-3.0/classes/Grid.html#Gtk.Grid.attach
    grid.attach(scrolled_window, left=0, top=0, width=8, height=10)
    grid.attach(button1, left=0, top=10, width=1, height=1)
    grid.attach(button2, left=1, top=10, width=1, height=1)
    grid.attach(button3, left=2, top=10, width=1, height=1)
    grid.attach(button4, left=3, top=10, width=1, height=1)
    grid.attach(button5, left=4, top=10, width=1, height=1)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

