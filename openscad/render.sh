#!/bin/sh

# Antialiased OpenSCAD rendering

# See http://talpadk.wordpress.com/2014/02/21/antialiased-openscad-rendering/

for FILE in $@
do
    if [ -f "${FILE}" ]
    then
        ls "${FILE}"
        PNG_FILE="${FILE}.png"
        openscad -o "${PNG_FILE}" --imgsize=2048,2048 "${FILE}"
        convert "${PNG_FILE}" -resize 512x512 "${PNG_FILE}"
    else
        echo "Error: ${FILE} is not a regular file."
    fi
done
