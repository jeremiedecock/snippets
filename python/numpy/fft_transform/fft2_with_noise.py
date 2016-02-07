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
#   ./fft2_with_noise.py -t 0.0001 -s ./test.jpeg
#   ./fft2_with_noise.py -t 0.001 ./test.jpeg
#   ipython3 -- ./fft2_with_noise.py -t 0.0001 -s ./test.jpeg
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
parser.add_argument("--noise", "-n",  help="The noise coefficient (between 0 and 1)", type=float, default=0, metavar="FLOAT")
parser.add_argument("fileargs", nargs=1, metavar="FILE", help="The file image to filter")
args = parser.parse_args()

shift = args.shift
noise_coefficient = args.noise
threshold = args.threshold
file_path = args.fileargs[0]

# GET DATA ###########################################################

# Open the image and convert it to grayscale
img = np.array(pil_img.open(file_path).convert('L'))

# Add noise
# TODO: lets the user choose the noise method : uniform, normal, poisson, ...
#noise = np.random.rand(*img.shape) * 255. * noise_coefficient
noise = np.random.poisson(255. * noise_coefficient, size=img.shape)

noised_img = img + noise

# Init plots
fig, ((ax1, ax4, ax7, ax10), (ax2, ax5, ax8, ax11), (ax3, ax6, ax9, ax12)) = plt.subplots(3, 4, figsize=(16, 10))

# Display images
ax1.imshow(img, interpolation='nearest', cmap=cm.gray)
ax1.set_title("Original image")

ax2.imshow(noise, interpolation='nearest', cmap=cm.gray)
ax2.set_title("Noise")

ax3.imshow(noised_img, interpolation='nearest', cmap=cm.gray)
ax3.set_title("Noised image")


# FOURIER TRANSFORM WITH NUMPY #######################################

# Do the fourier transform #############

fourier_img = np.fft.fft2(img)
fourier_noise = np.fft.fft2(noise)
fourier_noised_img = np.fft.fft2(noised_img)

if shift:
    fourier_img = np.fft.fftshift(fourier_img)
    fourier_noise = np.fft.fftshift(fourier_noise)
    fourier_noised_img = np.fft.fftshift(fourier_noised_img)

ax4.imshow(np.log10(abs(fourier_img)),
           interpolation='nearest',
           cmap=cm.gray)
ax4.set_title("Fourier coefficients\nbefore filtering (image)")

ax5.imshow(np.log10(abs(fourier_noise)),
           interpolation='nearest',
           cmap=cm.gray)
ax5.set_title("Fourier coefficients\nbefore filtering (noise)")

ax6.imshow(np.log10(abs(fourier_noised_img)),
           interpolation='nearest',
           cmap=cm.gray)
ax6.set_title("Fourier coefficients\nbefore filtering (noised image)")


# Filter ###############################

max_value = np.max(abs(fourier_img))

# TODO: lets the user choose between a threshold based on max, mean, median, ... or a geometric mask (square or circle to the center)
filtered_fourier_img = fourier_img * (abs(fourier_img) > max_value*threshold)
filtered_fourier_noise = fourier_noise * (abs(fourier_noise) > max_value*threshold)
filtered_fourier_noised_img = fourier_noised_img * (abs(fourier_noised_img) > max_value*threshold)

ax7.imshow(np.log10(abs(filtered_fourier_img)),
           interpolation='nearest',
           cmap=cm.gray)
ax7.set_title("Fourier coefficients\nafter filtering (image)")

ax8.imshow(np.log10(abs(filtered_fourier_noise)),
           interpolation='nearest',
           cmap=cm.gray)
ax8.set_title("Fourier coefficients\nafter filtering (noise)")

ax9.imshow(np.log10(abs(filtered_fourier_noised_img)),
           interpolation='nearest',
           cmap=cm.gray)
ax9.set_title("Fourier coefficients\nafter filtering (noised image)")


# Do the reverse transform #############

if shift:
    filtered_fourier_img = np.fft.ifftshift(filtered_fourier_img)
    filtered_fourier_noise = np.fft.ifftshift(filtered_fourier_noise)
    filtered_fourier_noised_img = np.fft.ifftshift(filtered_fourier_noised_img)

filtered_img = np.fft.ifft2(filtered_fourier_img)
filtered_noise = np.fft.ifft2(filtered_fourier_noise)
filtered_noised_img = np.fft.ifft2(filtered_fourier_noised_img)

ax10.imshow(abs(filtered_img), interpolation='nearest', cmap=cm.gray)
ax10.set_title("Filtered image")

ax11.imshow(abs(filtered_noise), interpolation='nearest', cmap=cm.gray)
ax11.set_title("Filtered noise")

ax12.imshow(abs(filtered_noised_img), interpolation='nearest', cmap=cm.gray)
ax12.set_title("Filtered noised image")


# SAVE FILES ######################

ax1.set_axis_off()
ax2.set_axis_off()
ax3.set_axis_off()
ax4.set_axis_off()
ax5.set_axis_off()
ax6.set_axis_off()

#ax7.set_axis_off()
#ax8.set_axis_off()
#ax9.set_axis_off()

ax10.set_axis_off()
ax11.set_axis_off()
ax12.set_axis_off()

#plt.savefig("fft2_with_noise.png")
#plt.savefig("fft2_with_noise.svg")
plt.savefig("fft2_with_noise.pdf")


# PLOT ############################

plt.show()


