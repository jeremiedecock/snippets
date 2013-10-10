#!/bin/bash

# Jeremie Decock 2013

# Print (recursively) jpeg file names sorted by creation date.


# TODO check $1
DIR=$1

get_date() {
    FILEPATH=$1
    DATETIME=$(exiftool "$FILEPATH" | grep "Create Date" | head -1 | cut -c 35-)
    
    # TODO: check datetime

    DATE=$(echo $DATETIME | cut -d " " -f 1 | tr ":" "/")
    TIME=$(echo $DATETIME | cut -d " " -f 2)

    # TODO: check date and time

    echo "$DATE $TIME   $FILEPATH"
}

find $DIR -type f -iregex ".*\.jpe?g" | while read FILE; do get_date "$FILE"; done
#find $DIR -type f -iregex ".*\.jpe?g" | while read FILE; do get_date "$FILE"; done | sort

