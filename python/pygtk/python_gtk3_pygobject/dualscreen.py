#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python GTK+3 snippet.

See: http://stackoverflow.com/questions/22772968/python-pygtk-how-to-put-a-window-on-a-specific-display-monitor
"""

from gi.repository import Gtk as gtk

def main():
    window1 = gtk.Window()
    window2 = gtk.Window()
    
    # Monitors
    screen = window1.get_screen()
    print("Screen size: ", screen.width(), " x ", screen.height())

    print("Monitors geometrie:")
    monitor_list = []
    for index, monitor in enumerate(range(screen.get_n_monitors())):
        monitor_geometry = screen.get_monitor_geometry(monitor)
        monitor_list.append(monitor_geometry)
        print(" monitor", index, " = height:", monitor_geometry.height, " width:", monitor_geometry.width, " x:", monitor_geometry.x, " y:", monitor_geometry.y)

    print(len(monitor_list), "monitors detected.")

    if(len(monitor_list) != 2):
        print("This snippet requires exactly 2 monitors.")
        sys.exit(1)

    window1.move(monitor_list[0].x, monitor_list[0].y)
    window2.move(monitor_list[1].x, monitor_list[1].y)

    window1.maximize()
    window2.maximize()

    window1.fullscreen()
    window2.fullscreen()

    print("Monitor of the current active window:", screen.get_monitor_at_window(screen.get_active_window()))

    # Label
    label1 = gtk.Label(label="Window1\n(press Alt+F4 to quit)")
    window1.add(label1)

    label2 = gtk.Label(label="Window2\n(press Alt+F4 to quit)")
    window2.add(label2)

    # Run
    window1.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window1.show_all()                             # display the window

    window2.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window2.show_all()                             # display the window

    gtk.main()                                    # GTK+ main loop

if __name__ == '__main__':
    main()

