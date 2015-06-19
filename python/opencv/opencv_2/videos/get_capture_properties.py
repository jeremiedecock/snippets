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

    # Get properties ######################################
    # See http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get

    # Resolution of the video stream
    width  = video_capture.get(cv.cv.CV_CAP_PROP_FRAME_WIDTH)
    height = video_capture.get(cv.cv.CV_CAP_PROP_FRAME_HEIGHT)
    print("Frame resolution:", width, "x", height)

    # Frame rate
    fps = video_capture.get(cv.cv.CV_CAP_PROP_FPS)
    print("Frame rate:", fps)

    # 4-character code of codec
    codec = video_capture.get(cv.cv.CV_CAP_PROP_FOURCC)
    print("Codec:", codec)

    # Brightness of the image (only for cameras)
    brightness = video_capture.get(cv.cv.CV_CAP_PROP_BRIGHTNESS)
    print("Brightness:", brightness)

    # Contrast of the image (only for cameras)
    contrast = video_capture.get(cv.cv.CV_CAP_PROP_CONTRAST)
    print("Contrast:", contrast)

    # Saturation of the image (only for cameras)
    saturation = video_capture.get(cv.cv.CV_CAP_PROP_SATURATION)
    print("Saturation:", saturation)

    # HUE of the image (only for cameras)
    hue = video_capture.get(cv.cv.CV_CAP_PROP_HUE)
    print("HUE:", hue)

    # Gain of the image (only for cameras)
    gain = video_capture.get(cv.cv.CV_CAP_PROP_GAIN)
    print("Gain:", gain)

    # Exposure of the image (only for cameras)
    exposure = video_capture.get(cv.cv.CV_CAP_PROP_EXPOSURE)
    print("Exposure:", exposure)

    #######################################################

    print()
    print("Press Q to quit.")

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
