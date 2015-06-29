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
import Tkinter as tk
import threading

def trackbar1_cb(x):
    pass

def trackbar2_cb(x):
    pass

#def scale_cb(ev=None):
#    print(scale.get())

def main():

    # Parse the programm options (get the path of the image file to read) #####

    parser = argparse.ArgumentParser(description='An opencv snippet.')
    parser.add_argument("--cameraid", "-i",  help="The camera ID number (default: 0)", type=int, default=0, metavar="INTEGER")
    args = parser.parse_args()

    device_number = args.cameraid

    # TkInter #################################################################

    root = tk.Tk()

    root.geometry("500x75")   # Set the size of the "root" window

    # See: http://effbot.org/tkinterbook/scale.htm
    scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL)
    #scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=scale_cb)
    scale.pack(fill=tk.X, expand=1)

    # OpenCV ##################################################################

    video_capture = cv.VideoCapture(device_number)

    # Create a window
    window_name = "Threshold Bin"
    cv.namedWindow(window_name)

    print("Press q to quit.")

    def opencv_main_loop():
        while(True):
            # Capture frame-by-frame.

            # 'ret' is a boolean ('True' if frame is read correctly, 'False' otherwise).
            # 'img_np' is an numpy array.
            ret, img_bgr = video_capture.read()

            # IMAGE PROCESSING ################################

            # Convert BGR color space to Grayscale
            img_gray = cv.cvtColor(img_bgr, cv.COLOR_BGR2GRAY)

            # Threshold the Grayscale image: dst_i = (src_i > threshold_value) ? max_val : 0
            threshold_value = scale.get()
            max_val =         255
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

    # Run the OpenCV main loop in a separate thread
    thread_cv = threading.Thread(target=opencv_main_loop)
    thread_cv.start()

    # Run the tkinter main loop
    root.mainloop()

if __name__ == '__main__':
    main()
