#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 dialog snippet.

See: http://python-gtk-3-tutorial.readthedocs.org/en/latest/dialogs.html
"""

from gi.repository import Gtk as gtk

def main():
    dialog = gtk.MessageDialog(parent=None, flags=0, message_type=gtk.MessageType.ERROR, buttons=gtk.ButtonsType.OK, message_format="This is an ERROR MessageDialog")
    dialog.format_secondary_text("And this is the secondary text that explains things.")
    dialog.run()
    dialog.destroy()

if __name__ == '__main__':
    main()

