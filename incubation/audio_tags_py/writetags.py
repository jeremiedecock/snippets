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

# TODO: handle unicode strings

import argparse
import os
import sys

import tagpy

DESCRIPTION = "Write audio tags."
EPILOG = "Please report bugs to <jd.jdhp@gmail.com>."
VERSION = "1.0"

def main():
    """Main function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument("file_paths", nargs='+', metavar="FILE", help="file to scan")
    parser.add_argument("--artist",  "-A",  help="artist tag",  metavar="STRING")
    parser.add_argument("--album",   "-a",  help="album tag",   metavar="STRING")
    parser.add_argument("--title",   "-T",  help="title tag",   metavar="STRING")
    parser.add_argument("--track",   "-t",  help="track tag",   metavar="INTEGER", type=int)
    parser.add_argument("--year",    "-y",  help="year tag",    metavar="INTEGER", type=int)
    parser.add_argument("--genre",   "-g",  help="genre tag",   metavar="STRING")
    parser.add_argument("--comment", "-c",  help="comment tag", metavar="STRING")

    args = parser.parse_args()

    for path in args.file_paths:
        if not os.path.isfile(path):
            print >> sys.stderr ,"ERROR: {0} is not a file.".format(path)
            print >> sys.stderr ,parser.format_usage(),
            sys.exit(2)

    # READ TAGS ###############################################################

    # For each path specified in command line argmuents
    for path in args.file_paths:

        print "artist :",  args.artist
        print "album :",   args.album
        print "title :",   args.title
        print "track :",   args.track
        print "year :",    args.year
        print "genre :",   args.genre
        print "comment :", args.comment

        try:
            file_ref = tagpy.FileRef(path)
            tags = file_ref.tag()

            if args.artist is not None:
                tags.artist  = args.artist.decode("utf-8")

            if args.album is not None:
                tags.album   = args.album.decode("utf-8")

            if args.title is not None:
                tags.title   = args.title.decode("utf-8")

            if args.track is not None:
                tags.track   = args.track

            if args.year is not None:
                tags.year    = args.year

            if args.genre is not None:
                tags.genre   = args.genre.decode("utf-8")

            if args.comment is not None:
                tags.comment = args.comment.decode("utf-8")

            file_ref.save()
        except ValueError as ex:
            print >> sys.stderr, "Wrong file format:", path
            #raise

if __name__ == '__main__':
    main()

