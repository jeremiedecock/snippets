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
#   ./fft_with_noise.py -t 0.0001 -s ./julie_lebrun.jpeg
#   ./fft_with_noise.py -t 0.001 ./julie_lebrun.jpeg
#   ipython3 -- ./fft_with_noise.py -t 0.0001 -s ./julie_lebrun.jpeg
#
# This snippet requires Numpy, Scipy, Matplotlib and PIL/Pillow Python libraries.
# 
# Additional documentation:
# - Numpy implementation: http://docs.scipy.org/doc/numpy/reference/routines.fft.html
# - Scipy implementation: http://docs.scipy.org/doc/scipy/reference/fftpack.html

import argparse

import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# PARSE OPTIONS ######################################################

parser = argparse.ArgumentParser(description='An FFT snippet.')

parser.add_argument("--shift", "-s", help="Shift the zero to the center", action="store_true", default=False)
parser.add_argument("--threshold", "-t",  help="The threshold value (between 0 and 1)", type=float, default=0, metavar="FLOAT")
parser.add_argument("--noise", "-n",  help="The noise coefficient (between 0 and 1)", type=float, default=0, metavar="FLOAT")
args = parser.parse_args()

shift = args.shift
noise_coefficient = args.noise
threshold = args.threshold

# GET DATA ###########################################################

# Make the signal
t = np.arange(5. * -math.pi, 5. * math.pi, 0.01)
#t = np.arange(0., 10. * math.pi, 0.01)
#sig = np.sin(t) + 2. * np.sin(2. * t) + 4. * np.sin(3. * t)
sig = np.cos(t) + 2. * np.cos(2. * t) + 4. * np.cos(3. * t)

# Add noise
# TODO: lets the user choose the noise method : uniform, normal, poisson, ...
#noise = np.random.poisson(1. * noise_coefficient, size=sig.shape)
noise = np.random.rand(*sig.shape) * noise_coefficient

noised_sig = sig + noise

# Init plots
fig, ((ax1, ax4, ax7, ax10), (ax2, ax5, ax8, ax11), (ax3, ax6, ax9, ax12)) = plt.subplots(3, 4, figsize=(16, 10))

# Display images
ax1.plot(t, sig)
ax1.set_title("Original signal")

ax2.plot(t, noise)
ax2.set_title("Noise")

ax3.plot(t, noised_sig)
ax3.set_title("Noised signal")


# FOURIER TRANSFORM WITH NUMPY #######################################

# Do the fourier transform #############

print(np.fft.rfft(sig))
print(type(np.fft.rfft(sig)[0]))

fourier_sig = np.fft.fft(sig)
fourier_noise = np.fft.fft(noise)
fourier_noised_sig = np.fft.fft(noised_sig)

if shift:
    fourier_sig = np.fft.fftshift(fourier_sig)
    fourier_noise = np.fft.fftshift(fourier_noise)
    fourier_noised_sig = np.fft.fftshift(fourier_noised_sig)

ax4.plot(t, abs(fourier_sig))
ax4.set_title("Fourier coefficients\nbefore filtering (signal)")

ax5.plot(t, abs(fourier_noise))
ax5.set_title("Fourier coefficients\nbefore filtering (noise)")

ax6.plot(t, abs(fourier_noised_sig))
ax6.set_title("Fourier coefficients\nbefore filtering (noised signal)")


# Filter ###############################

max_value = np.max(abs(fourier_sig))

# TODO: lets the user choose between a threshold based on max, mean, median, ... or a geometric mask (square or circle to the center)
filtered_fourier_sig = fourier_sig * (abs(fourier_sig) > max_value*threshold)
filtered_fourier_noise = fourier_noise * (abs(fourier_noise) > max_value*threshold)
filtered_fourier_noised_sig = fourier_noised_sig * (abs(fourier_noised_sig) > max_value*threshold)

ax7.plot(t, abs(filtered_fourier_sig))
ax7.set_title("Fourier coefficients\nafter filtering (signal)")

ax8.plot(t, abs(filtered_fourier_noise))
ax8.set_title("Fourier coefficients\nafter filtering (noise)")

ax9.plot(t, abs(filtered_fourier_noised_sig))
ax9.set_title("Fourier coefficients\nafter filtering (noised signal)")


# Do the reverse transform #############

if shift:
    filtered_fourier_sig = np.fft.ifftshift(filtered_fourier_sig)
    filtered_fourier_noise = np.fft.ifftshift(filtered_fourier_noise)
    filtered_fourier_noised_sig = np.fft.ifftshift(filtered_fourier_noised_sig)

filtered_sig = np.fft.ifft(filtered_fourier_sig)
filtered_noise = np.fft.ifft(filtered_fourier_noise)
filtered_noised_sig = np.fft.ifft(filtered_fourier_noised_sig)

ax10.plot(t, abs(filtered_sig))
ax10.set_title("Filtered signal")

ax11.plot(t, abs(filtered_noise))
ax11.set_title("Filtered noise")

ax12.plot(t, abs(filtered_noised_sig))
ax12.set_title("Filtered noised signal")


# SAVE FILES ######################

#ax1.set_axis_off()
#ax2.set_axis_off()
#ax3.set_axis_off()
#ax4.set_axis_off()
#ax5.set_axis_off()
#ax6.set_axis_off()

#ax7.set_axis_off()
#ax8.set_axis_off()
#ax9.set_axis_off()

#ax10.set_axis_off()
#ax11.set_axis_off()
#ax12.set_axis_off()

#plt.savefig("fft_with_noise.png")
#plt.savefig("fft_with_noise.svg")
plt.savefig("fft_with_noise.pdf")


# PLOT ############################

plt.show()


