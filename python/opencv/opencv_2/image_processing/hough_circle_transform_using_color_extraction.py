#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Extract one color.

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_houghcircles/py_houghcircles.html#hough-circles
     https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html#object-tracking

     http://txt.arboreus.com/2014/10/21/remove-circles-from-an-image-in-python.html
     http://wiki.elphel.com/index.php?title=OpenCV_Tennis_balls_recognizing_tutorial
     http://stackoverflow.com/questions/28521783/python-opencv-houghcircles-not-giving-good-results
     http://computer-vision-talks.com/articles/how-to-detect-circles-in-noisy-image/
     http://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
"""

from __future__ import print_function

import cv2 as cv
import numpy as np

def main():

# As said in https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html:
#
#   "In HSV, it is easier to represent a color than RGB color-space. In our
#   application, we will try to extract a blue colored object. So here is the
#   method:
#   
#   1. Take each frame of the video
#   2. Convert from BGR to HSV color-space
#   3. We threshold the HSV image for a range of blue color
#   4. Now extract the blue object alone, we can do whatever on that image we want."

# How to find HSV values to track?
#
#   As said in https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html:
#   This is a common question found in stackoverflow.com. It is very simple and
#   you can use the same function, cv2.cvtColor(). Instead of passing an image,
#   you just pass the BGR values you want. For example, to find the HSV value of
#   Green, try following commands in Python terminal:
#
#     >>> green = np.uint8([[[0,255,0 ]]])
#     >>> hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
#     >>> print hsv_green
#     [[[ 60 255 255]]]
#
#   Now you take [H-10, 100,100] and [H+10, 255, 255] as lower bound and upper
#   bound respectively. Apart from this method, you can use any image editing
#   tools like GIMP or any online converters to find these values, but don’t
#   forget to adjust the HSV ranges."

    device_number = 1
    video_capture = cv.VideoCapture(device_number)

    print("Press q to quit.")

    while(True):
        # Capture frame-by-frame.

        # 'ret' is a boolean ('True' if frame is read correctly, 'False' otherwise).
        # 'img_np' is an numpy array.
        ret, img_bgr = video_capture.read()

        # IMAGE PROCESSING ################################

        # Convert BGR color space to HSV
        img_hsv = cv.cvtColor(img_bgr, cv.COLOR_BGR2HSV)

        # Define range of blue color in HSV
        lower_blue = np.array([110, 50, 50])
        upper_blue = np.array([130, 255, 255])

        # Threshold the HSV image to get only blue colors
        img_mask = cv.inRange(img_hsv, lower_blue, upper_blue)

        # Hough Circle Transform
        method = cv.cv.CV_HOUGH_GRADIENT
        dp = 1.2
        min_dist = 300
        circles = cv.HoughCircles(img_mask, method, dp, min_dist, param1=50, param2=30, minRadius=0, maxRadius=0)

        # DRAW CIRCLES ####################################

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv.circle(img_bgr,(i[0],i[1]),i[2],(0,255,0),2)

                # draw the center of the circle
                cv.circle(img_bgr,(i[0],i[1]),2,(0,0,255),3)

        # DISPLAY IMAGES ##################################

        # Display the resulting frame (Mask)
        cv.imshow('Mask', img_mask)

        # Display the resulting frame (BGR)
        cv.imshow('BGR', img_bgr)

        # KEYBOARD LISTENER ###############################

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
