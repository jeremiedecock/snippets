#!/usr/bin/env python3
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

import argparse
import os
import sys

DESCRIPTION = "Rename files and directories recursively."
EPILOG = "Please report bugs to <jd.jdhp@gmail.com>."
VERSION = "1.0"

FILES_TO_BE_IGNORED = {"__init__.py"} 
DIRS_TO_BE_PRUNNED = {".git", ".svn"} 

CHARS_TO_BE_REMOVED = "|<>!?=@{}^%\\/$\a\b\f\n\r\v"
#CHARS_TO_BE_REPLACED = " \r&;`+#-:()'\""
CHARS_TO_BE_REPLACED = " \r&;`+#-:()[]\""
CHARS_TO_BE_UNDUPLICATED = "_."
CHARS_TO_BE_UNSTRIPPED = "_'"
STRINGS_TO_BE_REPLACED = {"_.": ".", "._": "."}

def rename(dirname, basename, dry_run=True):
    """Rename the file given in arguments."""

    if basename in FILES_TO_BE_IGNORED:
        return

    if len([chunk for chunk in os.path.split(dirname) if (chunk in FILES_TO_BE_IGNORED)]) > 0:
        return

    former_basename = basename
    former_path = os.path.join(dirname, basename)

    # Check whether or not former_path exists
    if not os.path.exists(former_path):
        print("Error", file=sys.stderr) # TODO

    ### RENAME ###

    # Remove invalid (ie. non-unicode) characters
    # TODO

    # Convert to lowercase
    basename = basename.lower()

    # Replace all occurrences of "bad" characters
    for forbidden_char in CHARS_TO_BE_REMOVED:
        basename = basename.replace(forbidden_char, "")

    for forbidden_char in CHARS_TO_BE_REPLACED:
        basename = basename.replace(forbidden_char, "_")

    # Remove duplicated (succecive) characters
    for duplicated_char in CHARS_TO_BE_UNDUPLICATED:
        # TODO: bug -> first and last char shoud be ignored
        basename = duplicated_char.join([elem for elem in basename.split(duplicated_char) if elem != ""])

    # Remove the leading and trailing characters
    basename = basename.strip(CHARS_TO_BE_UNSTRIPPED)

    # Replace all occurrences of "bad" strings
    for key, value in STRINGS_TO_BE_REPLACED.items():
        basename = basename.replace(key, value)

    ##############

    new_path = os.path.join(dirname, basename)

    if new_path != former_path:

        # Check whether or not new_path already exists
        if os.path.exists(new_path):
            print("Error", file=sys.stderr) # TODO

        print(former_basename, "->", basename)
        if not dry_run:
            pass # TODO

def main():
    """Main function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument("root_paths", nargs='+', metavar="DIRECTORY", help="directory to explore")
    parser.add_argument("--recursive", "-r",  help="recursive check", action="store_true")

    args = parser.parse_args()

    for path in args.root_paths:
        if args.recursive:
            # Recursive check -> args have to be directories
            if not os.path.isdir(path):
                parser.error("{0} is not a directory.".format(path))
        else:
            # Non recursive check -> args have to be files
            if not os.path.isfile(path):
                parser.error("{0} is not a file.".format(path))

    # WALK THROUGH THE TREES ##################################################

    # For each root path specified in command line argmuents
    for path in args.root_paths:

        if not args.recursive:
            # check the file
            rename(os.path.split(path))
        else:
            # walk through 'path':
            #  root =  a string, the path to the directory.
            #  dirs =  a list of the names (strings) of the subdirectories in
            #          dirpath (excluding '.' and '..').
            #  files = a list of the names (strings) of the non-directory files
            #          in dirpath.
            for root, dirs, files in os.walk(path, topdown=False):

                # Rename all files in the 'root' directory
                for file_str in files:
                    rename(root, file_str)

                # Rename all directories in the 'root' directory
                for dir_str in dirs:
                    rename(root, dir_str)

if __name__ == '__main__':
    main()

