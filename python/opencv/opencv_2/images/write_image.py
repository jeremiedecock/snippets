#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Write image: write an image given in arguments

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html#write-an-image
"""

from __future__ import print_function

import cv2 as cv
import argparse

def main():

    # Parse the programm options (get the path of the image files to read and write)

    parser = argparse.ArgumentParser(description='An opencv snippet.')
    parser.add_argument("--infile",  "-i",  help="The picture file to read",  required=True, metavar="FILE")
    parser.add_argument("--outfile", "-o",  help="The picture file to write", required=True, metavar="FILE")
    args = parser.parse_args()

    infile_str = args.infile
    outfile_str = args.outfile

    # OpenCV

    # imread_flags is a flag which specifies the way image should be read:
    # - cv.IMREAD_COLOR     loads a color image. Any transparency of image will be neglected. It is the default flag.
    # - cv.IMREAD_GRAYSCALE loads image in grayscale mode
    # - cv.IMREAD_UNCHANGED loads image as such including alpha channel
    imread_flags = cv.IMREAD_GRAYSCALE
    img_np_array = cv.imread(infile_str, imread_flags) # Read the image

    cv.imwrite(outfile_str, img_np_array) # Write the image

if __name__ == '__main__':
    main()
