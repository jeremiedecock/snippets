#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 Poppler snippet.

WARNING: Debian users have to install the "libpoppler-glib-dev" package to run
         this snippet.

SEE: http://stackoverflow.com/questions/9682297/displaying-pdf-files-with-python3
"""

import gi
gi.require_version('Poppler', '0.18')

from gi.repository import Gtk as gtk
from gi.repository import Poppler as poppler

import os

PDF_FILENAME = "test.pdf"

def main():
    window = gtk.Window()
    window.set_default_size(800, 600)

    # poppler
    pdfdoc = poppler.Document.new_from_file('file://' + os.path.abspath(PDF_FILENAME), password=None)
    print(pdfdoc.get_pdf_version_string())

    page = pdfdoc.get_page(0)

    # TODO: improve this... (use cairo ?)
    def draw(widget, surface):
        page.render(surface)

    window.connect("draw", draw)
    window.set_app_paintable(True)

    # main
    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

