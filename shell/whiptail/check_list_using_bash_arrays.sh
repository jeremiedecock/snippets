#!/bin/bash

# WARNING: the following file runs with Bash only

# If you are presenting a very long menu and want to make best use of the available screen, you can calculate the best box size by.
#   eval `resize`
#   whiptail ... $LINES $COLUMNS $(( $LINES - 8 )) ...

######

TITLE="Check list example"
SUB_TITLE="Choose user's permissions"
LABELS_ARRAY=(one two three four)
STATUS_ARRAY=(ON OFF ON OFF)

######

if [ ${#LABELS_ARRAY[@]} -ne ${#STATUS_ARRAY[@]} ]
then
    echo "Internal error, LABELS_ARRAY and STATUS_ARRAY don't have the same length."
    exit 1
fi

WHIPTAIL_CMD="whiptail --title \"${TITLE}\" --checklist "
WHIPTAIL_CMD+="\"${SUB_TITLE}\" 20 78 4 "

FIRST_INDEX=0
LAST_INDEX=$(( ${#LABELS_ARRAY[@]} - 1 ))

for INDEX in $(seq ${FIRST_INDEX} ${LAST_INDEX})
do
    PRINT_INDEX=$(( $INDEX + 1 ))
    WHIPTAIL_CMD+="\"$PRINT_INDEX\" \"${LABELS_ARRAY[$INDEX]}\" ${STATUS_ARRAY[$INDEX]} "
done

WHIPTAIL_CMD+="3>&1 1>&2 2>&3 "

### DEBUG ###
#echo "${WHIPTAIL_CMD}"
#eval ${WHIPTAIL_CMD}

CHOICE=$(eval ${WHIPTAIL_CMD})

#CHOICE=$(whiptail --title "Check list example" --checklist \
#                          "Choose user's permissions" 20 78 4 \
#                          "NET_OUTBOUND" "Allow connections to other hosts" ON \
#                          "NET_INBOUND" "Allow connections from other hosts" OFF \
#                          "LOCAL_MOUNT" "Allow mounting of local devices" OFF \
#                          "REMOTE_MOUNT" "Allow mounting of remote devices" OFF 3>&1 1>&2 2>&3)

echo "CHOICE: $CHOICE"

