#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 Webkit snippet.

WARNING: Debian users have to install the "libwebkitgtk-3.0-dev" package to run
         this snippet.
"""

import gi
gi.require_version('WebKit', '3.0')

from gi.repository import Gtk as gtk
from gi.repository import WebKit as webkit

HTML = """<html><body><h1>Hello</h1></body></html>"""

def main():
    window = gtk.Window()
    window.set_default_size(800, 600)

    # webkit
    webview = webkit.WebView()
    webview.load_html_string(HTML, '')

    # scrolled window
    scrolled_window = gtk.ScrolledWindow()
    scrolled_window.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.AUTOMATIC)  # should be gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS or gtk.PolicyType.NEVER
    scrolled_window.add(webview)

    window.add(scrolled_window)

    # main
    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

