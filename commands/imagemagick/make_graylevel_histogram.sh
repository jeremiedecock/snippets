#!/bin/sh

# See: http://www.imagemagick.org/Usage/files/#histogram

convert test.jpeg -colorspace Gray -define histogram:unique-colors=false histogram:histogram_gray.gif
