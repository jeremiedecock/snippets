#!/bin/sh

INDEX=0
mkdir tmp

for FILE in *.JPG
do
    NUM=$(printf %04d $INDEX)
    #ln "$FILE" ./tmp/img_${NUM}.jpeg
    #cp "$FILE" ./tmp/img_${NUM}.jpeg
    echo "$FILE -> ./tmp/img_${NUM}.jpeg"
    convert "$FILE" -resize 1920x1080\! ./tmp/img_${NUM}.jpeg
    #mogrify -resize 1920x1080 ./tmp/img_${NUM}.jpeg
    #mogrify -resize 800x600 ./tmp/img_${NUM}.jpeg
    INDEX=$(($INDEX+1))
done

avconv -f image2 -i ./tmp/img_%04d.jpeg video.mp4

rm -rf tmp
