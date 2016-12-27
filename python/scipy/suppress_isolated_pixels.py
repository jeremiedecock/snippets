#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.label.html#scipy.ndimage.label
#      https://docs.scipy.org/doc/scipy/reference/tutorial/ndimage.html#segmentation-and-labeling

import numpy as np
from scipy.ndimage import label, generate_binary_structure

a = np.array([[0,0,1,1,0,0],
              [0,0,0,1,0,0],
              [1,1,0,0,1,0],
              [0,0,0,1,0,0]])

labeled_array, num_features = label(a)

print(labeled_array)
print(num_features)
