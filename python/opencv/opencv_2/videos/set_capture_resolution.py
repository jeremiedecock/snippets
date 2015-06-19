#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Capture video: capture videos from camera

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html#capture-video-from-camera
"""

from __future__ import print_function

import cv2 as cv

def main():

    device_number = 0
    video_capture = cv.VideoCapture(device_number)

    # Set the resolution ##################################
    # See http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get
    width  = video_capture.get(cv.cv.CV_CAP_PROP_FRAME_WIDTH)
    height = video_capture.get(cv.cv.CV_CAP_PROP_FRAME_HEIGHT)
    print("Former frame resolution:", width, "x", height)

    video_capture.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    video_capture.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

    width  = video_capture.get(cv.cv.CV_CAP_PROP_FRAME_WIDTH)
    height = video_capture.get(cv.cv.CV_CAP_PROP_FRAME_HEIGHT)
    print("New frame resolution:", width, "x", height)
    #######################################################

    print("Press q to quit.")

    while(True):
        # Capture frame-by-frame.

        # 'ret' is a boolean ('True' if frame is read correctly, 'False' otherwise).
        # 'img_np' is an numpy array.
        ret, img_np = video_capture.read()

        # Display the resulting frame
        cv.imshow('video capture snippet', img_np)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
