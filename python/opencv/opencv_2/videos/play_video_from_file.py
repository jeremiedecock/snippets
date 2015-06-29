#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Play video: play videos from files

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html#playing-video-from-file
"""

from __future__ import print_function

import cv2 as cv
import argparse

def main():

    # Parse the programm options (get the path of the image file to read) #####

    parser = argparse.ArgumentParser(description='An opencv snippet.')
    parser.add_argument("--infile", "-i",  help="The video file to play", required=True, metavar="FILE")
    args = parser.parse_args()

    infile_str = args.infile

    # OpenCV ##################################################################

    video_capture = cv.VideoCapture(infile_str)

    #framerate = 25
    framerate = video_capture.get(cv.cv.CV_CAP_PROP_FPS)

    print("Press q to quit.")

    while(True):
        # Capture frame-by-frame.

        # 'ret' is a boolean ('True' if frame is read correctly, 'False' otherwise).
        # 'img_np' is an numpy array.
        ret, img_np = video_capture.read()

        # Display the resulting frame
        cv.imshow('video capture snippet', img_np)
        if cv.waitKey(int(1000./framerate)) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()

