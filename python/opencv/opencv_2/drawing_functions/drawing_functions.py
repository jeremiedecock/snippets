#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
OpenCV - Drawing functions: draw lines, circles, rectangles, ellipses and text

Required: opencv library (Debian: aptitude install python-opencv)

See: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_drawing_functions/py_drawing_functions.html
"""

from __future__ import print_function

import cv2 as cv
import numpy as np

def main():

    # Common arguments:
    # - points : (0,0) is at the top left
    # - color : use a tuple for BGR, eg: (255,0,0) for blue. For grayscale, just pass the scalar value.
    # - thickness : thickness of the line. If -1 is passed for closed figures like circles, it will fill the shape.
    # - lineType : type of line, whether 8-connected, anti-aliased line etc. By default, it is 8-connected. cv2.LINE_AA gives anti-aliased line which looks great for curves.

    # CREATE A BLACK IMAGE
    img_np = np.zeros((512, 512, 3), np.uint8)

    # DRAW A LINE
    point_1 = (0, 0)
    point_2 = (256, 256)
    color = (0, 0, 255)
    thickness = 3
    cv.line(img_np, point_1, point_2, color, thickness)

    # DRAW A RECTANGLE
    point_1 = (300, 100)
    point_2 = (400, 400)
    color = (255, 0, 0)
    thickness = -1
    cv.rectangle(img_np, point_1, point_2, color, thickness)

    # DRAW A CIRCLE
    center_point = (100, 300)
    radius = 64
    color = (0, 255, 0)
    thickness = 2
    cv.circle(img_np, center_point, radius, color, thickness)

    line_type = cv.CV_AA  # Anti-Aliased
    cv.circle(img_np, center_point, radius + 20, color, thickness, line_type)

    # DRAW A ELLIPSE
    center_point = (200, 400)
    axes_length = (100, 50)
    angle = 45 # the angle of rotation of ellipse in anti-clockwise direction
    start_angle = 0
    end_angle = 180
    color = (255, 255, 0)
    thickness = 3
    line_type = cv.CV_AA  # Anti-Aliased
    cv.ellipse(img_np, center_point, axes_length, angle, start_angle, end_angle, color, thickness, line_type)

    # DRAW A POLYGON
    pts = np.array([[32,87], [124,81], [75,43], [60,11]], np.int32)
    pts = pts.reshape((-1,1,2))

    is_closed = True
    color = (255, 0, 255)
    thickness = 3
    line_type = cv.CV_AA  # Anti-Aliased

    cv.polylines(img_np, [pts], is_closed, color, thickness, line_type)

    # ADD TEXT
    text = "Hello!"
    start_point = (150, 500)
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 4
    color = (255, 0, 255)
    thickness = 3
    line_type = cv.CV_AA  # Anti-Aliased
    cv.putText(img_np, text, start_point, font, font_scale, color, thickness, line_type)

    # SAVE THE IMAGE 
    cv.imwrite("out.png", img_np)

if __name__ == '__main__':
    main()
