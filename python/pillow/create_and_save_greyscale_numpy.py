#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

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

import PIL.Image as pil_img     # PIL.Image is a module not a class...
import numpy as np

SIZE_X = 320
SIZE_Y = 200


def normalize(array):
    """Normalize the values of a Numpy array in the range [0,1].

    Parameters
    ----------
    array : array like
        The array to normalize

    Returns
    -------
    ndarray
        The normalized array
    """
    min_value = array.min()
    max_value = array.max()
    size = max_value - min_value

    if size > 0:
        array = array.astype('float64', copy=True)
        norm_array = (array - min_value)/size
    else:
        norm_array = array

    return norm_array


def main():
    """Main function"""

    # Make the data
    image_array = np.random.normal(size=(SIZE_Y, SIZE_X))

    # Make the data (pixels value in [0;255])
    image_array = normalize(image_array) * 255.
    image_array = image_array.astype('uint8', copy=True)
    print(image_array)

    # Make the image
    mode = "L"              # Grayscale
    size_y, size_x = image_array.shape
    image_pil = pil_img.new(mode, (size_x, size_y))

    # WARNING: nested list and 2D numpy arrays are silently rejected!!!
    #          data *must* be a list or a 1D numpy array!
    image_pil.putdata(image_array.flatten()) 

    # Save the image
    image_pil.save("create_and_save_greyscale_numpy.png")

if __name__ == '__main__':
    main()
