#!/bin/sh

# The values given to --menu are:
# - The text describing the menu ("Choose an option")
# - The height of the dialog (20)
# - The width of the dialog (78)
# - The height of the menu list (16)
# The rest of the values are a list of menu options in the format tag item,
# where tag is the name of the option which is printed to stderr when selected,
# and item is the description of the menu option.
#
# If you are presenting a very long menu and want to make best use of the available screen, you can calculate the best box size by.
#   eval `resize`
#   whiptail ... $LINES $COLUMNS $(( $LINES - 8 )) ...

CHOICE=$(whiptail --title "Menu example" --menu "Choose an option" 25 78 16 \
                          "<-- Back" "Return to the main menu." \
                          "Add User" "Add a user to the system." \
                          "Modify User" "Modify an existing user." \
                          "List Users" "List all users on the system." \
                          "Add Group" "Add a user group to the system." \
                          "Modify Group" "Modify a group and its list of members." \
                          "List Groups" "List all groups on the system." 3>&1 1>&2 2>&3)

echo $CHOICE
