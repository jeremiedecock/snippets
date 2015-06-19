#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Display image: display an image given in arguments

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html#display-an-image
"""

from __future__ import print_function

import cv2 as cv
import argparse
from matplotlib import pyplot as plt

def main():

    # Parse the programm options (get the path of the image file to display)

    parser = argparse.ArgumentParser(description='An opencv snippet.')
    parser.add_argument("--infile", "-i",  help="The picture file to display", required=True, metavar="FILE")
    args = parser.parse_args()

    infile_str = args.infile

    # OpenCV

    # imread_flags is a flag which specifies the way image should be read:
    # - cv.IMREAD_COLOR     loads a color image. Any transparency of image will be neglected. It is the default flag.
    # - cv.IMREAD_GRAYSCALE loads image in grayscale mode
    # - cv.IMREAD_UNCHANGED loads image as such including alpha channel
    imread_flags = cv.IMREAD_GRAYSCALE
    img_np = cv.imread(infile_str, imread_flags)

    plt.imshow(img_np, cmap='gray', interpolation='none')  # Display the image "img_np" with matplotlib
    plt.xticks([])        # to hide tick values on X axis
    plt.yticks([])        # to hide tick values on Y axis
    plt.show()

if __name__ == '__main__':
    main()
