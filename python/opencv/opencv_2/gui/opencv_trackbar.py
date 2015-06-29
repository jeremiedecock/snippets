#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Trackbar widget.

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_trackbar/py_trackbar.html#trackbar
"""

from __future__ import print_function

import cv2 as cv
import numpy as np
import argparse

def trackbar1_cb(x):
    pass

def trackbar2_cb(x):
    pass

def main():

    # Parse the programm options (get the path of the image file to read) #####

    parser = argparse.ArgumentParser(description='An opencv snippet.')
    parser.add_argument("--cameraid", "-i",  help="The camera ID number (default: 0)", type=int, default=0, metavar="INTEGER")
    args = parser.parse_args()

    device_number = args.cameraid

    # OpenCV ##################################################################

    video_capture = cv.VideoCapture(device_number)

    # Create a window
    window_name = "Threshold Bin"
    cv.namedWindow(window_name)

    # Create trackbars
    trackbar1_name = "Threshold"
    trackbar1_window_name = window_name
    trackbar1_default_value = 127
    trackbar1_maximum_value = 255
    trackbar1_callback_function = trackbar1_cb     # Executed everytime trackbar value changes
    cv.createTrackbar(trackbar1_name, trackbar1_window_name, trackbar1_default_value, trackbar1_maximum_value, trackbar1_callback_function)

    trackbar2_name = "Max value"
    trackbar2_window_name = window_name
    trackbar2_default_value = 255
    trackbar2_maximum_value = 255
    trackbar2_callback_function = trackbar2_cb     # Executed everytime trackbar value changes
    cv.createTrackbar(trackbar2_name, trackbar2_window_name, trackbar2_default_value, trackbar2_maximum_value, trackbar2_callback_function)

    print("Press q to quit.")

    while(True):
        # Capture frame-by-frame.

        # 'ret' is a boolean ('True' if frame is read correctly, 'False' otherwise).
        # 'img_np' is an numpy array.
        ret, img_bgr = video_capture.read()

        # IMAGE PROCESSING ################################

        # Convert BGR color space to Grayscale
        img_gray = cv.cvtColor(img_bgr, cv.COLOR_BGR2GRAY)

        # Threshold the Grayscale image: dst_i = (src_i > threshold_value) ? max_val : 0
        threshold_value = cv.getTrackbarPos(trackbar1_name, trackbar1_window_name)
        max_val =         cv.getTrackbarPos(trackbar2_name, trackbar2_window_name)
        ret, img_threshold_bin = cv.threshold(img_gray, threshold_value, max_val, cv.THRESH_BINARY)

        # DISPLAY IMAGES ##################################

        # Display the resulting frame (BGR)
        cv.imshow('BGR (orignal)', img_bgr)

        # Display the resulting frames (Threshold)
        cv.imshow(window_name, img_threshold_bin)

        # KEYBOARD LISTENER ###############################

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
