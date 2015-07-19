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


# See http://stackoverflow.com/questions/4764932/in-python-how-do-i-read-the-exif-data-for-an-image/4765242#4765242

import PIL.Image as pil_img     # PIL.Image is a module not a class...

import PIL
import PIL.ExifTags

def main():
    """Main function"""

    img = pil_img.open("test.jpeg")

    # Print the image's EXIF metadata dictionary indexed by EXIF numeric tags
    exif_data_num_dict = img._getexif()
    print(exif_data_num_dict)

    # Print the image's EXIF metadata dictionary indexed by EXIF tag name strings
    exif_data_str_dict = {PIL.ExifTags.TAGS[k]: v for k, v in exif_data_num_dict.items() if k in PIL.ExifTags.TAGS}
    print(exif_data_str_dict)

if __name__ == '__main__':
    main()
