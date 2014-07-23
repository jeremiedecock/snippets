#!/bin/bash

# If you are presenting a very long menu and want to make best use of the available screen, you can calculate the best box size by.
#   eval `resize`
#   whiptail ... $LINES $COLUMNS $(( $LINES - 8 )) ...

eval `resize`
#                  filename height width
whiptail --scrolltext --textbox ~/.bashrc $(( $LINES - 8 )) $(( $COLUMNS - 8 ))
