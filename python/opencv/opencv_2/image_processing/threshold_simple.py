#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Simple thresholding.

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#simple-thresholding
     Oreilly's book "Learning OpenCV" (first edition) p.135 for details about Thresholding.
"""

from __future__ import print_function

import cv2 as cv
import numpy as np
import argparse

def main():

    # Parse the programm options (get the path of the image file to read) #####

    parser = argparse.ArgumentParser(description='An opencv snippet.')
    parser.add_argument("--cameraid", "-i",  help="The camera ID number (default: 0)", type=int, default=0, metavar="INTEGER")
    args = parser.parse_args()

    device_number = args.cameraid

    # OpenCV ##################################################################

    video_capture = cv.VideoCapture(device_number)

    print("Press q to quit.")

    while(True):
        # Capture frame-by-frame.

        # 'ret' is a boolean ('True' if frame is read correctly, 'False' otherwise).
        # 'img_np' is an numpy array.
        ret, img_bgr = video_capture.read()

        # IMAGE PROCESSING ################################

        # Convert BGR color space to Grayscale
        img_gray = cv.cvtColor(img_bgr, cv.COLOR_BGR2GRAY)

        # Threshold the Grayscale image (when thersholding, "source image should be gray")
        # THRESH_BINARY:     dst_i = (src_i > threshold_value) ? max_val : 0
        # THRESH_BINARY_INV: dst_i = (src_i > threshold_value) ? 0 : max_val
        # THRESH_TRUNC:      dst_i = (src_i > threshold_value) ? threshold_value : src_i
        # THRESH_TOZERO:     dst_i = (src_i > threshold_value) ? src_i : 0
        # THRESH_TOZERO_INV: dst_i = (src_i > threshold_value) ? 0 : src_i
        threshold_value = 127
        max_val = 255             # The value to be given if pixel value is more than the threshold value (only concerns THRESH_BINARY and THRESH_BINARY_INV)
        ret, img_threshold_bin         = cv.threshold(img_gray, threshold_value, max_val, cv.THRESH_BINARY)
        ret, img_threshold_bin_inv     = cv.threshold(img_gray, threshold_value, max_val, cv.THRESH_BINARY_INV)
        ret, img_threshold_trunc       = cv.threshold(img_gray, threshold_value, max_val, cv.THRESH_TRUNC)
        ret, img_threshold_to_zero     = cv.threshold(img_gray, threshold_value, max_val, cv.THRESH_TOZERO)
        ret, img_threshold_to_zero_inv = cv.threshold(img_gray, threshold_value, max_val, cv.THRESH_TOZERO_INV)

        # DISPLAY IMAGES ##################################

        # Display the resulting frame (BGR)
        cv.imshow('BGR (orignal)', img_bgr)

        # Display the resulting frames (Threshold)
        cv.imshow('Threshold Bin', img_threshold_bin)
        cv.imshow('Threshold Bin Inv', img_threshold_bin_inv)
        cv.imshow('Threshold Trunc', img_threshold_trunc)
        cv.imshow('Threshold To Zero', img_threshold_to_zero)
        cv.imshow('Threshold To Zero Inv', img_threshold_to_zero_inv)

        # KEYBOARD LISTENER ###############################

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
