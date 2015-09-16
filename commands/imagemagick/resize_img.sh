#!/bin/sh

for FILE in "$@"
do
    #ls ${FILE}
    convert ${FILE} -resize 25% small_${FILE}
done
