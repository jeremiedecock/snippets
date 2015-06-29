#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Adaptive thresholding.

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#adaptive-thresholding
     Oreilly's book "Learning OpenCV" (first edition) p.138 for details about Adaptive Thresholding.
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

        # Threshold the Grayscale image (when thersholding, "source image
        # should be gray").
        # Adaptive thresholding is a good alternative to simple thresholding
        # when image has different lighting conditions in different areas.
        # Adaptive threshold algorithm calculates the threshold for a small
        # regions of the image. So we get different thresholds for different
        # regions of the same image and it gives us better results for images
        # with varying illumination.
        # - Adaptive methods: cv.ADAPTIVE_THRESH_MEAN_C or cv.ADAPTIVE_THRESH_GAUSSIAN_C (weighted mean)
        # - Threshold types: 
        #      cv.THRESH_BINARY:     dst_i = (src_i > threshold_value) ? max_val : 0
        #      cv.THRESH_BINARY_INV: dst_i = (src_i > threshold_value) ? 0 : max_val
        #      cv.THRESH_TRUNC:      dst_i = (src_i > threshold_value) ? threshold_value : src_i
        #      cv.THRESH_TOZERO:     dst_i = (src_i > threshold_value) ? src_i : 0
        #      cv.THRESH_TOZERO_INV: dst_i = (src_i > threshold_value) ? 0 : src_i
        max_value = 255             # The value to be given if pixel value is more than the threshold value (only concerns THRESH_BINARY and THRESH_BINARY_INV)
        block_size = 11
        adaptive_param = 2
        img_adaptive_threshold_mean     = cv.adaptiveThreshold(img_gray, max_value, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, block_size, adaptive_param)
        img_adaptive_threshold_gaussian = cv.adaptiveThreshold(img_gray, max_value, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, block_size, adaptive_param)

        # DISPLAY IMAGES ##################################

        # Display the resulting frame (BGR)
        cv.imshow('BGR (orignal)', img_bgr)

        # Display the resulting frames (Threshold)
        cv.imshow('Adaptive Threshold Mean', img_adaptive_threshold_mean)
        cv.imshow('Adaptive Threshold Gaussian', img_adaptive_threshold_gaussian)

        # KEYBOARD LISTENER ###############################

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
