#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Otsu’s Binarization.

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#otsus-binarization
"""

from __future__ import print_function

import cv2 as cv
import numpy as np
import argparse

PLOT_HIST = False

if PLOT_HIST:
    import matplotlib.pyplot as plt

def main():

    # Parse the programm options (get the path of the image file to read) #####

    parser = argparse.ArgumentParser(description='An opencv snippet.')
    parser.add_argument("--cameraid", "-i",  help="The camera ID number (default: 0)", type=int, default=0, metavar="INTEGER")
    args = parser.parse_args()

    device_number = args.cameraid

    # Matplotlib ##############################################################

    if PLOT_HIST:
        plt.ion()    # setup interactive mode
        plt.show()

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
        # "In global thresholding, we used an arbitrary value for threshold
        # value, right? So, how can we know a value we selected is good or not?
        # Answer is, trial and error method. But consider a bimodal image (In
        # simple words, bimodal image is an image whose histogram has two
        # peaks). For that image, we can approximately take a value in the
        # middle of those peaks as threshold value, right ? That is what Otsu
        # binarization does. So in simple words, it automatically calculates a
        # threshold value from image histogram for a bimodal image. (For images
        # which are not bimodal, binarization won’t be accurate.)"
        # (src: https://opencv-python-tutroals.readthedocs.org)
        max_value = 255             # The value to be given if pixel value is more than the threshold value (only concerns THRESH_BINARY and THRESH_BINARY_INV)
        threshold_value = 0         # 0 = use Otsu's Binarization
        computed_threshold, img_otsu = cv.threshold(img_gray, threshold_value, max_value, cv.THRESH_BINARY + cv.THRESH_OTSU)

        # Otsu’s Binarization with Gaussian blur
        img_blur = cv.GaussianBlur(img_gray, (5,5), 0)
        computed_threshold, img_blur_otsu = cv.threshold(img_blur, threshold_value, max_value, cv.THRESH_BINARY + cv.THRESH_OTSU)

        # DISPLAY IMAGES ##################################

        # Display the resulting frame (BGR)
        cv.imshow('BGR (orignal)', img_bgr)

        # Display the resulting frames (Threshold)
        cv.imshow('Otsu’s Binarization', img_otsu)

        # Display the resulting frames (Threshold)
        cv.imshow('Otsu’s Binarization with Gaussian Blur', img_blur_otsu)

        if PLOT_HIST:
            plt.clf()
            plt.hist(img_gray.ravel(), 256)
            #plt.hist(img_blur.ravel(), 256)
            plt.draw()

        print("Computed threshold:", computed_threshold)

        # KEYBOARD LISTENER ###############################

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
