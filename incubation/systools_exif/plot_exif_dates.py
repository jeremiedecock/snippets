#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

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

# PLOT EXIF DATES
#    Plot the number of picture files created everyday (according to EXIF
#    data) from a given directory (and recursively all it's subdirectories).

# TODO
# - plot one graph per month (otherwise it will be difficult to read it)

# OVERVIEW
# 1. build the dictionary {'filepath': date, ...}:
#    -> walk tree (looking for *.jp[e]g files only)
#    -> use "date = get_exif_date('filepath')"
#       -> return date or None there is no valid EXIF data
# 2. for each dictionary's item (ie. for each file with valid EXIF data):
#    -> TODO

import os
import sys
import argparse
import warnings

import datetime
#import operator

import Image
import PIL
import PIL.ExifTags

VERSION = "1.0"
COPYING = '''Copyright (c) 2013 Jeremie DECOCK (http://www.jdhp.org)
This is free software; see the source for copying conditions.
There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.'''

# Only considers files having one of these extensions
FILE_NAME_EXTENSIONS = ('.jpg', '.jpeg')

# For the tag name, see http://www.w3.org/2003/12/exif/
#EXIF_DATETIME_TAG = 'DateTimeDigitized'
EXIF_DATETIME_TAG = 'DateTimeOriginal'

def custom_formatwarning(message, category, filename, lineno, line=""):
    """Ignore everything except the message."""
    return "Warning: " + str(message) + "\n"

def main():
    """Main function"""

    warnings.formatwarning = custom_formatwarning

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Sort all picture files (with valid EXIF data) from a given directory (and recursively all it's subdirectories).")

    parser.add_argument("--version", "-v", action="version", version="%(prog)s " + VERSION)
    parser.add_argument("directories_path", nargs="*", metavar="DIRECTORY", help="root directory")

    args = parser.parse_args()

    # CHECK ROOT_PATHS
    for path in args.directories_path:
        if not os.path.isdir(path):
            parser.error("{0} is not a directory.".format(path))

    # BUILD {PATH:DATE,...} DICTIONARY (WALK THE TREE) ########################

    date_list = []

    # For each root path specified in command line argmuents
    for path in args.directories_path:
        local_date_list = walk(path)
        date_list.extend(local_date_list)

    date_dict = {}
    for exif_date in date_list:
        if exif_date in date_dict:
            date_dict[exif_date] += 1
        else:
            date_dict[exif_date] = 1
    
    plot(date_dict)


# PLOT ########################################################################

def plot(date_dict):
    #for exif_date, num in sorted(date_dict.iteritems(), key=operator.itemgetter(0)):
    if None in date_dict:
        print date_dict[None], "errors"
        del date_dict[None]

    for exif_date, num in sorted(date_dict.items(), key=lambda x: x[0]):
        print exif_date.strftime("%d/%m/%Y"), num


# EXIF UTILITIES ##############################################################

def get_exif_date(file_path):
    """Get the exif creation date.
    
    This implementation use PIL (Python Imaging Library).
    For an other implementation, see: http://stackoverflow.com/questions/765396/exif-manipulation-library-for-python

    Returns None if the file doesn't have valid EXIF data.
    """

    exif_date = None

    try:
        img = Image.open(file_path)

        # Metadata dictionary indexed by EXIF numeric tags
        exif_data_num_dict = img._getexif()

        if exif_data_num_dict is not None:

            # Metadata dictionary indexed by EXIF tag name strings
            exif_data_str_dict = {PIL.ExifTags.TAGS[k].lower() : v for k, v in exif_data_num_dict.items() if k in PIL.ExifTags.TAGS}   # uses lower to avoid case errors

            if EXIF_DATETIME_TAG.lower() in exif_data_str_dict:
                exif_datetime = exif_data_str_dict[EXIF_DATETIME_TAG.lower()]   # uses lower to avoid case errors
                exif_date = datetime.datetime.strptime(exif_datetime.split()[0], "%Y:%m:%d")

    except AttributeError:
        pass   # raised by "img._getexif()"
    except ValueError:
        pass   # raised by "datetime.datetime.strptime(...)"
    except IOError:
        pass   # raised by "Image.open(...)"

    return exif_date

# TOOLS #######################################################################

# BUILD {PATH:MD5,...} DICTIONARY (WALK THE TREE) #########################

def walk(root_path):
    """Walk the tree starting from "root_path" and build the {path:date,...}
    dictionary"""

    local_date_list = []
    
    # current_dir_path = a string, the path to the directory.
    # dir_names        = a list of the names (strings) of the subdirectories in
    #                    current_dir_path (excluding '.' and '..').
    # file_names       = a list of the names (strings) of the non-directory files
    #                    in current_dir_path.
    for current_dir_path, dir_names, file_names in os.walk(root_path, topdown=False, followlinks=False):

        # ABSOLUTE PATH OF current_dir_path
        current_dir_path = os.path.abspath(current_dir_path)

        # CHILD FILES
        file_names = [file_name for file_name in file_names if file_name.lower().endswith(FILE_NAME_EXTENSIONS)]    # *.jp[e]g files only!

        for file_name in file_names:
            file_path = os.path.join(current_dir_path, file_name)
            
            if not os.path.islink(file_path):
                file_date = get_exif_date(file_path)
                local_date_list.append(file_date)
#            else:
#                warnings.warn("ignore link " + file_path, UserWarning)

    return local_date_list


if __name__ == '__main__':
    main()

