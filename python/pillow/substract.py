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

import argparse
import os.path
import PIL.Image as pil_img     # PIL.Image is a module not a class...
import numpy as np

def main():
    """Main function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description='An argparse snippet.')

    parser.add_argument("--mask", "-m", required=True, metavar="FILE",
                        help="The file used as a mask")
    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="the files to process")

    args = parser.parse_args()

    mask_path = args.mask
    file_paths = args.fileargs

    # PROCESS #################################################################

    np_img_mask = np.array(pil_img.open(mask_path))

    for file_path in file_paths:
        img = pil_img.open(file_path)

        np_img = np.array(img)
        np_img = np_img - np_img_mask

        img = pil_img.fromarray(np_img)

        output_filename = "out_" + os.path.basename(file_path)
        img.save(output_filename)

if __name__ == '__main__':
    main()

