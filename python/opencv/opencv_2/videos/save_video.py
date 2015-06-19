#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Save video: capture and save videos from camera

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html#playing-video-from-fi
"""

from __future__ import print_function

import cv2 as cv

def main():

    device_number = 0
    video_capture = cv.VideoCapture(device_number)

    print("Press q to quit.")

    # DEFINE THE CODEC, FRAMERATE AND RESOLUTION + CREATE VIDEOWRITER OBJECT

    # See: http://www.fourcc.org/codecs.php
    fourcc = cv.cv.CV_FOURCC('X', 'V', 'I', 'D')

    fps = 20.

    #resolution = (640, 480)
    width  = int(video_capture.get(cv.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv.cv.CV_CAP_PROP_FRAME_HEIGHT))
    resolution = (width, height)

    video_writer = cv.VideoWriter('capture.avi', fourcc, fps, resolution)

    #######################################################

    while(video_capture.isOpened()):
        # Capture frame-by-frame.

        # 'ret' is a boolean ('True' if frame is read correctly, 'False' otherwise).
        # 'img_np' is an numpy array.
        ret, img_np = video_capture.read()

        if ret == True:
            video_writer.write(img_np)

            # Display the resulting frame
            cv.imshow('video capture snippet', img_np)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    video_capture.release()
    video_writer.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
