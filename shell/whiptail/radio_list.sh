#!/bin/sh

# If you are presenting a very long menu and want to make best use of the available screen, you can calculate the best box size by.
#   eval `resize`
#   whiptail ... $LINES $COLUMNS $(( $LINES - 8 )) ...

CHOICE=$(whiptail --title "Check list example" --radiolist \
                          "Choose user's permissions" 20 78 4 \
                          "NET_OUTBOUND" "Allow connections to other hosts" ON \
                          "NET_INBOUND" "Allow connections from other hosts" OFF \
                          "LOCAL_MOUNT" "Allow mounting of local devices" OFF \
                          "REMOTE_MOUNT" "Allow mounting of remote devices" OFF 3>&1 1>&2 2>&3)

echo $CHOICE
