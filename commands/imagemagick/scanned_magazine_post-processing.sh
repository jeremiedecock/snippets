#!/bin/sh

# Additionnal documentation:
# - http://www.scantips.com/basics6b.html
# - http://www.scantips.com/basics6c.html
#
#   "Traditional procedures to eliminate moiré patterns without the Descreen
#   filter often include scanning at 2X or more the desired resolution, apply a
#   blur or despeckle filter, resample to half size to get the desired final
#   size, then use a sharpening filter"
#
# - http://www.descreen.net/eng/soft/descreen/descreen.htm
# - http://www.fmwconcepts.com/imagemagick/fftfilter/index.php
# - http://www.fmwconcepts.com/imagemagick/fourier_transforms/fourier.html
# - http://www.imagemagick.org/Usage/fourier/
#
# Keywords: descreen, halftone, moiré

# Scan at 300dpi (choose a PNG output format).
# This script will downscale the scanned images at 150dpi.

if [ "$#" -lt "1" ]; then
    echo "Error: wrong number of parameters" >&2
    echo "USAGE: $0 FILE1 [FILE2 ...]" >&2
    exit 1
fi

for IN_FILE in "$@"
do
    OUT_FILE=$(echo ${IN_FILE} | sed "s/.png$/.jpeg/")
    convert "${IN_FILE}" -blur 1x1 -despeckle -filter gaussian -define filter:sigma=0.375 -define filter:blur=0.75 -resize 50% -enhance -quality 80 "${OUT_FILE}"
done

# Reference:
# - convert in.png -blur 1x1 -despeckle -filter gaussian -define filter:sigma=0.375 -define filter:blur=0.75 -resize 50% -enhance -quality 80 out.jpeg
#   (output=298.3 ko for the test image)
#
# Alternatives:
# - convert in.png -blur 1x1 -despeckle -resize 50% -enhance -quality 80 out.jpeg
#   (output=306.7 ko for the test image)
# - convert in.png -blur 1x1 -resize 50% -quality 80 out.jpeg
#   (output=316.4 ko for the test image)
# - convert in.png -blur 1x1 -despeckle -resize 50% -quality 80 out.jpeg
#   (output=309.7 ko for the test image)
# - convert in.png -blur 1x1 -despeckle -resize 50% -sharpen 0x1.0 -enhance -quality 80 out.jpeg
#   (output=346.1 ko for the test image)
# - convert in.png -blur 1x1 -despeckle -filter mitchell -resize 50% -enhance -quality 80 out.jpeg
#   (output=289.5 ko for the test image)

