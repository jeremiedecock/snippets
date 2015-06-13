#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
A simple Python GTK+3 SpinButton snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/button_widgets.html#spinbutton

API doc:
- Gtk.SpinButton: http://lazka.github.io/pgi-docs/Gtk-3.0/classes/SpinButton.html#Gtk.SpinButton
- Gtk.Adjustment: http://lazka.github.io/pgi-docs/Gtk-3.0/classes/Adjustment.html#Gtk.Adjustment
"""

from gi.repository import Gtk as gtk

def numeric_toggled_cb(src_widget, data):
    """
    Sets the flag that determines if non-numeric text can be typed into the
    spin button.
    """

    spin_button = data
    check_button = src_widget

    spin_button.set_numeric(check_button.get_active())

def if_valid_toggled_cb(src_widget, data):
    """
    Sets the update behavior of a spin button. This determines whether the spin
    button is always updated or only when a valid value is set.
    """

    spin_button = data
    check_button = src_widget

    if check_button.get_active():
        policy = gtk.SpinButtonUpdatePolicy.IF_VALID
    else:
        policy = gtk.SpinButtonUpdatePolicy.ALWAYS
    spin_button.set_update_policy(policy)

def print_button_cb(src_widget, data):
    spin_button = data

    print("value: " + str(spin_button.get_value()))

def reset_button_cb(src_widget, data):
    spin_button = data

    spin_button.set_value(0.)

def main():
    window = gtk.Window()
    window.set_border_width(10)

    # SpinButton
    spin_button = gtk.SpinButton()

    # step (float) = increment applied for a button 1 press.
    # page (float) = increment applied for a button 2 press.
    spin_button.set_increments(step=0.1, page=1.)
    spin_button.set_range(min=0., max=100.)
    spin_button.set_digits(2)   # Set the number of digits after the decimal point to be displayed for the spin button’s value
    spin_button.set_value(0.)

    ## Alternative:
    #adjustment = gtk.Adjustment(value=0., lower=0., upper=100., step_increment=0.1, page_increment=10., page_size=0.)
    #spin_button.set_adjustment(adjustment)

    # Check numeric
    check_numeric = gtk.CheckButton(label="Numeric")
    check_numeric.connect("toggled", numeric_toggled_cb, spin_button)  # connect("event", callback, data)

    # Check if valid
    check_if_valid = gtk.CheckButton(label="If valid")
    check_if_valid.connect("toggled", if_valid_toggled_cb, spin_button)  # connect("event", callback, data)

    # Print button
    print_button = gtk.Button(label="Print")
    print_button.connect("clicked", print_button_cb, spin_button)  # connect("event", callback, data)

    # Clear button
    reset_button = gtk.Button(label="Reset")
    reset_button.connect("clicked", reset_button_cb, spin_button)  # connect("event", callback, data)

    # Grid
    grid = gtk.Grid()
    grid.set_column_spacing(6)
    grid.set_row_spacing(6)
    window.add(grid)

    grid.attach(spin_button,    left=0, top=0, width=1, height=1)
    grid.attach(check_numeric,  left=1, top=0, width=1, height=1)
    grid.attach(check_if_valid, left=2, top=0, width=1, height=1)
    grid.attach(print_button,   left=0, top=1, width=3, height=1)
    grid.attach(reset_button,   left=0, top=2, width=3, height=1)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

