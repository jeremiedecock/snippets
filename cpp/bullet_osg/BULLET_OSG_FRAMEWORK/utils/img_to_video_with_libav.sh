#!/bin/bash

#FILENAME_PREFIX="screen_shot_0_"
#FILE_EXT_IN="jpg"
FILENAME_PREFIX="capture_0_"
FILE_EXT_IN="png"

#RESOLUTION="1920x1080"
RESOLUTION="512x512"

INDEX=0
mkdir tmp

# TODO: improve this ugly workaround...
for FILE in ${FILENAME_PREFIX}[0-9].${FILE_EXT_IN} ${FILENAME_PREFIX}[0-9][0-9].${FILE_EXT_IN} ${FILENAME_PREFIX}[0-9][0-9][0-9].${FILE_EXT_IN}
do
    NUM=$(printf %04d $INDEX)

    echo "$FILE -> ./tmp/img_${NUM}.jpeg"
    convert "$FILE" -resize ${RESOLUTION}\! ./tmp/img_${NUM}.jpeg
    #mogrify -resize 1920x1080 ./tmp/img_${NUM}.jpeg
    INDEX=$(($INDEX+1))
done

avconv -f image2 -i ./tmp/img_%04d.jpeg video.mp4

rm -rf tmp
