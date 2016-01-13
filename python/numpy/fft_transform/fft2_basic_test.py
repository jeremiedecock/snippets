#!/usr/bin/env python3

# Fast Fourier Transform snippets
# 
# Documentation:
# - Numpy implementation: http://docs.scipy.org/doc/numpy/reference/routines.fft.html
# - Scipy implementation: http://docs.scipy.org/doc/scipy/reference/fftpack.html

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 8))

# MAKE DATA ##########################################################

pattern = np.zeros((4, 4))
pattern[1:3,1:3] = 1

signal = np.tile(pattern, (2, 2))

ax1.imshow(signal, interpolation='nearest', cmap=cm.gray)
ax1.set_title("Original image")


# FOURIER TRANSFORM WITH NUMPY #######################################
 

# Do the fourier transform #############

transformed_signal = np.fft.fft2(signal)

ax2.imshow(abs(transformed_signal), interpolation='nearest', cmap=cm.gray)
ax2.set_title("Fourier coefficients before filtering")

#shifted_transformed_signal = np.fft.fftshift(transformed_signal)
#shifted_filtered_signal = np.fft.ifftshift(transformed_signal)


# Filter ###############################

max_value = np.max(abs(transformed_signal))
filtered_transformed_signal = transformed_signal * (abs(transformed_signal) > max_value*0.5)

ax3.imshow(abs(filtered_transformed_signal), interpolation='nearest', cmap=cm.gray)
ax3.set_title("Fourier coefficients after filtering")


# Do the reverse transform #############

filtered_signal = np.fft.ifft2(filtered_transformed_signal)

ax4.imshow(abs(filtered_signal), interpolation='nearest', cmap=cm.gray)
ax4.set_title("Filtered image")

plt.show()

