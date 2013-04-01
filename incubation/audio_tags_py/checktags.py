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

import argparse
import os
import sys

import tagpy

DESCRIPTION = "Check whether or not an audio file has tags."
EPILOG = "Please report bugs to <jd.jdhp@gmail.com>."
VERSION = "1.0"

CHECK_ARTIST_TAG = False
CHECK_ALBUM_TAG = False
CHECK_TITLE_TAG = False
CHECK_TRACK_TAG = False
CHECK_YEAR_TAG = False
CHECK_GENRE_TAG = False
CHECK_COMMENT_TAG = False

def check_path(path):
    """Check if the given path has required tags."""
    try:
        file_ref = tagpy.FileRef(path)
        tags = file_ref.tag()

        failed = False

        if CHECK_ARTIST_TAG and len(tags.artist.strip()) == 0:
            failed = True

        if CHECK_ALBUM_TAG and len(tags.album.strip()) == 0:
            failed = True

        if CHECK_TITLE_TAG and len(tags.title.strip()) == 0:
            failed = True

        if CHECK_TRACK_TAG and tags.track == 0:
            failed = True

        if CHECK_YEAR_TAG and tags.year == 0:
            failed = True

        if CHECK_GENRE_TAG and len(tags.genre.strip()) == 0:
            failed = True

        if CHECK_COMMENT_TAG and len(tags.comment.strip()) == 0:
            failed = True

        if failed:
            print path

    except ValueError:
        print >> sys.stderr, "Wrong file format:", path


def main():
    """Main function"""

    global CHECK_ARTIST_TAG
    global CHECK_ALBUM_TAG
    global CHECK_TITLE_TAG
    global CHECK_TRACK_TAG
    global CHECK_YEAR_TAG
    global CHECK_GENRE_TAG
    global CHECK_COMMENT_TAG

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument("file_paths", nargs='+', metavar="FILE", help="file to scan")
    parser.add_argument("--recursive", "-r",  help="recursive check", action="store_true")
    parser.add_argument("--artist",    "-A",  help="artist tag",      action="store_true")
    parser.add_argument("--album",     "-a",  help="album tag",       action="store_true")
    parser.add_argument("--title",     "-T",  help="title tag",       action="store_true")
    parser.add_argument("--track",     "-t",  help="track tag",       action="store_true")
    parser.add_argument("--year",      "-y",  help="year tag",        action="store_true")
    parser.add_argument("--genre",     "-g",  help="genre tag",       action="store_true")
    parser.add_argument("--comment",   "-c",  help="comment tag",     action="store_true")

    args = parser.parse_args()

    for path in args.file_paths:
        if args.recursive:
            # Recursive check -> args have to be directories
            if not os.path.isdir(path):
                parser.error("{0} is not a directory.".format(path))
        else:
            # Non recursive check -> args have to be files
            if not os.path.isfile(path):
                parser.error("{0} is not a file.".format(path))

    if not (args.artist or args.album or args.title or args.track or args.year or args.genre or args.comment):
        parser.error("One of --artist, --album, --title, --track, --year, --genre or --comment must be given")

    CHECK_ARTIST_TAG =  args.artist
    CHECK_ALBUM_TAG =   args.album
    CHECK_TITLE_TAG =   args.title
    CHECK_TRACK_TAG =   args.track
    CHECK_YEAR_TAG =    args.year 
    CHECK_GENRE_TAG =   args.genre
    CHECK_COMMENT_TAG = args.comment

    # READ TAGS ###############################################################

    # For each path specified in command line argmuents
    for path in args.file_paths:

        if not args.recursive:
            # check the file
            check_path(path)
        else:
            # walk through 'path':
            #  root =  a string, the path to the directory.
            #  dirs =  a list of the names (strings) of the subdirectories in
            #          dirpath (excluding '.' and '..').
            #  files = a list of the names (strings) of the non-directory files
            #          in dirpath.
            for root, dirs, files in os.walk(path, topdown=False):
                for file_str in files:
                    check_path(os.path.join(root, file_str))

if __name__ == '__main__':
    main()

