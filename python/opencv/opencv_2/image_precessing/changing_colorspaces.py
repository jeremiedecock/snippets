#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Changing colorspaces: convert images from one color-space to another

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html#converting-colorspaces
"""

from __future__ import print_function

import cv2 as cv

def main():

    device_number = 0
    video_capture = cv.VideoCapture(device_number)

    print("Press q to quit.")

    while(True):
        # Capture frame-by-frame.

        # 'ret' is a boolean ('True' if frame is read correctly, 'False' otherwise).
        # 'img_np' is an numpy array.
        ret, img_bgr = video_capture.read()

        # Display the resulting frame (BGR)
        cv.imshow('BGR (orignal)', img_bgr)

        # Display the resulting frame (Gray)
        img_gray = cv.cvtColor(img_bgr, cv.COLOR_BGR2GRAY)
        cv.imshow('Gray', img_gray)

        # Display the resulting frame (HSV)
        img_hsv = cv.cvtColor(img_bgr, cv.COLOR_BGR2HSV)
        cv.imshow('HSV', img_hsv)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
