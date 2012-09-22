#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Jérémie DECOCK (http://www.jdhp.org)

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
import os
import sys

DESCRIPTION = "Walk through a directory tree."
EPILOG = "Please report bugs to <jd.jdhp@gmail.com>."
VERSION = "1.0"

def main():
    """Main function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument("root_paths", nargs='+', metavar="DIRECTORY", help="directory to explore")
    args = parser.parse_args()

    for path in args.root_paths:
        if not os.path.isdir(path):
            print "ERROR: {0} is not a directory.".format(path)
            print parser.format_usage(),
            sys.exit(2)

    # WALK THROUGH THE TREES ##################################################

    # For each root path specified in command line argmuents
    for path in args.root_paths:

        # Walk through 'path':
        #  root =  a string, the path to the directory.
        #  dirs =  a list of the names (strings) of the subdirectories in
        #          dirpath (excluding '.' and '..').
        #  files = a list of the names (strings) of the non-directory files
        #          in dirpath.
        for root, dirs, files in os.walk(path, topdown=False):

            print root

            # Print all directories in the 'root' directory
            for dir_str in dirs:
                print " " * 3, "[dir]", os.path.join(root, dir_str)

            # Print all files in the 'root' directory
            for file_str in files:
                print " " * 3, "[file]", os.path.join(root, file_str)


if __name__ == '__main__':
    main()

