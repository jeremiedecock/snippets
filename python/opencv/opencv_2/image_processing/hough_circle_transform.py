#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Hough Circle Transform: find circles in an image.

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_houghcircles/py_houghcircles.html#hough-circles
"""

from __future__ import print_function

import cv2 as cv
import numpy as np

def main():

    device_number = 0
    video_capture = cv.VideoCapture(device_number)

    # Reduce the video resolution
    video_capture.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    video_capture.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

    print("Press q to quit.")

    while(True):
        # Capture frame-by-frame.

        # 'ret' is a boolean ('True' if frame is read correctly, 'False' otherwise).
        # 'img_np' is an numpy array.
        ret, img_bgr = video_capture.read()

        # IMAGE PROCESSING ################################

        # Convert BGR color space to HSV
        img_gray = cv.cvtColor(img_bgr, cv.COLOR_BGR2GRAY)

        # Hough Circle Transform
        circles = cv.HoughCircles(img_gray, cv.cv.CV_HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

        # DRAW CIRCLES ####################################

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv.circle(img_bgr,(i[0],i[1]),i[2],(0,255,0),2)

                # draw the center of the circle
                cv.circle(img_bgr,(i[0],i[1]),2,(0,0,255),3)

        # DISPLAY IMAGES ##################################

        # Display the resulting frame (BGR)
        cv.imshow('BGR (orignal)', img_bgr)

        # KEYBOARD LISTENER ###############################

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
