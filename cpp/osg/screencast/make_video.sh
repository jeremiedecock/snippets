#!/bin/sh

PREFIX=capture

ffmpeg2theora -v 9 -f image2 ${PREFIX}_%04d.png -o ${PREFIX}.ogv
