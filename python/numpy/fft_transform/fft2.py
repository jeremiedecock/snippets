#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Fast Fourier Transform snippet
#
# Example usages:
#   ./fft2.py -t 0.0001 -s ./lenna.png
#   ./fft2.py -t 0.001 ./lenna.png
#   ipython3 -- ./fft2.py -t 0.0001 -s ./lenna.png
#
# This snippet requires Numpy, Scipy, Matplotlib and PIL/Pillow Python libraries.
# 
# Additional documentation:
# - Numpy implementation: http://docs.scipy.org/doc/numpy/reference/routines.fft.html
# - Scipy implementation: http://docs.scipy.org/doc/scipy/reference/fftpack.html

import argparse

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import PIL.Image as pil_img     # PIL.Image is a module not a class...

# PARSE OPTIONS ######################################################

parser = argparse.ArgumentParser(description='An FFT snippet.')

parser.add_argument("--shift", "-s", help="Shift the zero to the center", action="store_true", default=False)
parser.add_argument("--threshold", "-t",  help="The threshold value (between 0 and 1)", type=float, default=0, metavar="FLOAT")
parser.add_argument("fileargs", nargs=1, metavar="FILE", help="The file image to filter")
args = parser.parse_args()

shift = args.shift
threshold = args.threshold
file_path = args.fileargs[0]


# GET DATA ###########################################################

# Open the image and convert it to grayscale
signal = np.array(pil_img.open(file_path).convert('L'))

# Init plot
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 8))

# Plot
ax1.imshow(signal, interpolation='nearest', cmap=cm.gray)
ax1.set_title("Original image")


# FOURIER TRANSFORM WITH NUMPY #######################################

# Do the fourier transform #############

transformed_signal = np.fft.fft2(signal)

if shift:
    transformed_signal = np.fft.fftshift(transformed_signal)

ax2.imshow(np.log10(abs(transformed_signal)),
           interpolation='nearest',
           cmap=cm.gray)
ax2.set_title("Fourier coefficients before filtering")


# Filter ###############################

max_value = np.max(abs(transformed_signal))
filtered_transformed_signal = transformed_signal * (abs(transformed_signal) > max_value*threshold)

ax3.imshow(np.log10(abs(filtered_transformed_signal)),
           interpolation='nearest',
           cmap=cm.gray)
ax3.set_title("Fourier coefficients after filtering")


# Do the reverse transform #############

if shift:
    filtered_transformed_signal = np.fft.ifftshift(filtered_transformed_signal)

filtered_signal = np.fft.ifft2(filtered_transformed_signal)

ax4.imshow(abs(filtered_signal), interpolation='nearest', cmap=cm.gray)
ax4.set_title("Filtered image")


# SAVE FILES ######################

#plt.savefig("fft2.png")
#plt.savefig("fft2.svg")
plt.savefig("fft2.pdf")


# PLOT ############################

plt.show()

