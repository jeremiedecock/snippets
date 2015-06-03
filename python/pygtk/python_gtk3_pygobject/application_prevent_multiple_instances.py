#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: http://stackoverflow.com/questions/19072161/preventing-multiple-instances-of-a-gtk-application
     https://developer.gnome.org/gnome-devel-demos/stable/GtkApplicationWindow.py.html.en
     https://git.gnome.org/browse/gnome-music/tree/gnomemusic/application.py
     https://git.gnome.org/browse/pitivi/tree/pitivi/application.py
     https://git.gnome.org/browse/gnome-tweak-tool/tree/gtweak/app.py
     https://git.gnome.org/browse/meld/tree/meld/meldapp.py
"""

from gi.repository import Gtk as gtk
from gi.repository import Gio as gio
import sys

class MyWindow(gtk.ApplicationWindow):
    """
    An ApplicationWindow...
    """

    def __init__(self, app):
        gtk.Window.__init__(self, title="Hello World!", application=app) # window belongs to the application "app"
        self.set_default_size(200, 100)

        # create a label
        label = gtk.Label(label="Hello GNOME!")
        self.add(label)


class MyApplication(gtk.Application):
    """
    Gtk.Application initializes GTK+. It also connects the x button that's
    automatically generated along with the window to the "destroy" signal.
    """

    def __init__(self):
        gtk.Application.__init__(self, application_id="org.jdhp.test", flags=gio.ApplicationFlags.FLAGS_NONE)

        self._window = None

    def do_activate(self):
        """
        Create and activate a MyWindow, with self (the MyApplication) as
        application the window belongs to.
        Note that the function in C activate() becomes do_activate() in Python.
        """
        if not self._window:
            self._window = MyWindow(self)
            self._window.show_all()       # this line could go in the constructor of MyWindow as well
        else:
            print("DEBUG: the window already exists.")

    def do_startup(self):
        """
        Start up the application.
        Note that the function in C startup() becomes do_startup() in Python.
        """
        gtk.Application.do_startup(self)


def main():
    # Create and run the application
    application = MyApplication()

    print("Application id:", application.get_application_id())

    exit_status = application.run(sys.argv)
    sys.exit(exit_status)

if __name__ == '__main__':
    main()

