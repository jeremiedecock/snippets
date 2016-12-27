#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.label.html#scipy.ndimage.label
#      https://docs.scipy.org/doc/scipy/reference/tutorial/ndimage.html#segmentation-and-labeling

import numpy as np
from scipy import ndimage

###############################################################################

def kill_isolated_pixels(array,
                         structure=None,
                         threshold=0.2):
    """
    Return array with isolated islands removed.
    Only keeping the biggest islands (largest surface).

    :param array: Array with completely isolated cells
    :param struct: Structure array for generating unique regions
    :return: Filtered array with just the largest island
    """

    filtered_array = np.copy(array)

    # Put to 0 pixels that are below 'threshold'
    filtered_array[filtered_array < threshold] = 0
    mask = filtered_array > 0

    # Detect islands ("label")
    label_array, num_labels = ndimage.label(mask, structure=structure)

    # Count the number of pixels for each island
    num_pixels_per_island = ndimage.sum(filtered_array, label_array, range(num_labels + 1))

    # Only keep the biggest island
    mask_biggest_island = num_pixels_per_island < np.max(num_pixels_per_island)
    remove_pixel = mask_biggest_island[label_array]

    filtered_array[remove_pixel] = 0

    return filtered_array

###############################################################################

array = np.array([[0,0,1,1,0,0],
                  [0,0,0,1,0,0],
                  [1,1,0,0,1,0],
                  [0,0,0,1,0,0]])

#structure = np.ones((3, 3))
#print("structure:\n", structure)

print("array:\n", array)

filtered_array = kill_isolated_pixels(array)

print("filtered_array:\n", filtered_array)
