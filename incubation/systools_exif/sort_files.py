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

# SORT_FILES
#    Sort all picture files (with valid EXIF data) from a given directory (and
#    recursively all it's subdirectories).
#    This program generate a new directory tree and move all picture files there.
#    Sort is done according to EXIF creation dates.
#
#    Make directories for each year and sub directories for each month.
#
#    For instance, this kind of directory tree is generated:
#
#         sorted
#          |- 2000
#          |   |- 03
#          |   |   |- 188984.jpg
#          |   |   |- 188985.jpg
#          |   |   |- 188986.jpg
#          |   |   `- 188987.jpg
#          |   |- 05
#          |   |   |- 188988.jpg
#          |   |   |- 188990.jpg
#          |   |   |- 188991.jpg
#          |   |   `- 188992.jpg
#          |   `- 07
#          |       |- 188993.jpg
#          |       |- 188994.jpg
#          |       |- 188995.jpg
#          |       `- 188996.jpg
#          `- 2001
#              |- 2|00
#              |   |- 189001.jpg
#              |   |- 189002.jpg
#              |   |- 189003.jpg
#              |   `- 189004.jpg
#              `- 2|00
#                  |- 189005.jpg
#                  |- 189005.jpg
#                  |- 189005.jpg
#                  `- 189005.jpg

# TODO
#    - keep unknown files in place (ie. files with invalid EXIF data)
#    - add a text file in each directory (append if it already exists) with the
#      original path of each file (sorted) -> this can help to remember the
#      context (place, ...) of photos
#    - remove empty directories
#    - handle clone files (2 files with the same name in the same output directory)
#      -> add a suffix if the MD5SUM is not the same, keep only one otherwise

# OVERVIEW
# 1. build the dictionary {'filepath': date, ...}:
#    -> walk tree (looking for *.jp[e]g files only)
#    -> use "date = get_exif_date('filepath')"
#       -> return date or None there is no valid EXIF data
# 2. for each dictionary's item (ie. for each file with valid EXIF data):
#    -> make the destination directory if it doesn't exist
#    -> move the file

import os
import sys
import argparse
import warnings

import datetime

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

    file_dict = {}   # dict = {filepath: date, ...}

    # For each root path specified in command line argmuents
    for path in args.directories_path:
        local_file_dict = walk(path)
        file_dict.update(local_file_dict)

    for file_path, exif_date in file_dict.items():
        move_file(file_path, exif_date)


# FILE TREATMENT ##############################################################

def move_file(file_path, exif_date):
    # TODO
    # For each dictionary's item (ie. for each file with valid EXIF data):
    #    -> make the destination directory if it doesn't exist
    #    -> move the file
    print exif_date.strftime("%d/%m/%Y"), file_path

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

    local_file_dict = {}   # dict = {path: date, ...}
    
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
                local_file_dict[file_path] = file_date
#            else:
#                warnings.warn("ignore link " + file_path, UserWarning)

    return local_file_dict


if __name__ == '__main__':
    main()

