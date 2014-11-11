#!/bin/bash

# Antialiased OpenSCAD rendering

# See http://talpadk.wordpress.com/2014/02/21/antialiased-openscad-rendering/

for FILE in "$@"
do
    # http://stackoverflow.com/questions/407184/how-to-determine-file-type-in-bash-script
    if [[ "$FILE" == *.scad ]]
    then
        ls "${FILE}"
        PNG_FILE="$(basename "${FILE}" .scad).png"
        openscad -o "${PNG_FILE}" --imgsize=2048,2048 "${FILE}"

        if [ -s "${PNG_FILE}" ]
        then
            convert "${PNG_FILE}" -resize 512x512 "${PNG_FILE}"
        else
            rm -v "${PNG_FILE}"
        fi
    else
        echo "Error: ${FILE} is not an OpenSCAD file."
    fi
done
