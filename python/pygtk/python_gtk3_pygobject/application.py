#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: https://developer.gnome.org/gnome-devel-demos/stable/window.py.html.en
"""

from gi.repository import Gtk as gtk
import sys

class MyApplication(gtk.Application):
    """
    Gtk.Application initializes GTK+. It also connects the x button that's
    automatically generated along with the window to the "destroy" signal.
    """

    def do_activate(self):
        window = gtk.Window(application=self)
        window.set_title("Welcome to GNOME")
        window.show_all()


def main():
    # Create and run the application
    application = MyApplication()
    exit_status = application.run(sys.argv)
    sys.exit(exit_status)

if __name__ == '__main__':
    main()

