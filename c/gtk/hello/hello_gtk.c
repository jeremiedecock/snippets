/* 
 * HelloGTK: a very basic GTK snippet.
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Require: libgtk-3-dev (Debian)
 * Usage:   gcc hello_gtk.c -o hello_gtk $(pkg-config --cflags --libs gtk+-3.0)
 *
 * See http://developer.gnome.org/gtk3/stable/ for more info
 *
 */

#include <gtk/gtk.h>

int main(int argc, char * argv[])
{
    GtkWidget * window;
    GtkWidget * label;

    gtk_init(&argc, &argv);

    /* Create the main, top level window */
    window = gtk_window_new(GTK_WINDOW_TOPLEVEL);

    /* Give it a title */
    gtk_window_set_title(GTK_WINDOW(window), "Hello GTK");

    /* Set the default size of the window */
    gtk_window_set_default_size(GTK_WINDOW(window), 300, 200);

    /* Map the destroy signal of the window to gtk_main_quit */
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    /* Make a label widget */
    label = gtk_label_new("Hello!");

    /* Put the label onto the main window */
    gtk_container_add(GTK_CONTAINER(window), label);

    /* Make sure that everything, window and label, are visible */
    gtk_widget_show_all(window);

    /* Start the main loop */
    gtk_main();

    return 0;
}
