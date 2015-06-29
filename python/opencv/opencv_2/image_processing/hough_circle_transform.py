#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Hough Circle Transform: find circles in an image.

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_houghcircles/py_houghcircles.html#hough-circles
     Oreilly's book "Learning OpenCV" (first edition) p.158 for details about Hough transforms.
"""

from __future__ import print_function

import cv2 as cv
import numpy as np
import argparse

def main():

    # Parse the programm options (get the path of the image file to read)

    parser = argparse.ArgumentParser(description='An opencv snippet.')
    parser.add_argument("--cameraid", "-i",  help="The camera ID number (default: 0)", type=int, default=0, metavar="INTEGER")
    args = parser.parse_args()

    device_number = args.cameraid

    # OpenCV

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
        # See Oreilly's book "Learning OpenCV" (first edition) p.158 for details about Hough transforms.
        # - method : the only method available is CV_HOUGH_GRADIENT so...
        # - dp : the resolution of the accumumator image used (allow to create
        #   an accumulator of a lower resolution than the input image). It must
        #   be greater or equal to 1. A value of "1" keep the original size; a
        #   value of "2" divide the resolution by 2, ...
        # - min_dist : the minimum distance between 2 circles (distances in
        #   pixels). Should be proportional to the image size (img_bgr.shape[0]
        #   and img_bgr.shape[1]).
        # - param1 : the edge (Canny) threshold.
        # - param2 : the accumulator threshold.
        # - minRadius : the minimum radius of circles that can be found (radius
        #   in pixels). Should be proportional to the image size
        #   (img_bgr.shape[0] and img_bgr.shape[1]).
        # - maxRadius : the maximum radius of circles that can be found (radius
        #   in pixels). Should be proportional to the image size
        #   (img_bgr.shape[0] and img_bgr.shape[1]).
        method = cv.cv.CV_HOUGH_GRADIENT  # The only method available is CV_HOUGH_GRADIENT.
        dp = 1                            # The resolution of the accumumator.
        min_dist = 20                     # The minimum distance between 2 circles (in pixels).
        canny_edge_threshold = 50
        accumulator_threshold = 30
        min_radius = 0
        max_radius = 0
        #circles = cv.HoughCircles(img_gray, method, dp, min_dist)
        circles = cv.HoughCircles(img_gray, method, dp, min_dist, param1=canny_edge_threshold, param2=accumulator_threshold, minRadius=min_radius, maxRadius=max_radius)

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
