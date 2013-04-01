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

def main():
    """Main function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument("file_paths", nargs='+', metavar="FILE", help="file to scan")
    parser.add_argument("--artist",  "-A",  help="artist tag",  action="store_true")
    parser.add_argument("--album",   "-a",  help="album tag",   action="store_true")
    parser.add_argument("--title",   "-T",  help="title tag",   action="store_true")
    parser.add_argument("--track",   "-t",  help="track tag",   action="store_true")
    parser.add_argument("--year",    "-y",  help="year tag",    action="store_true")
    parser.add_argument("--genre",   "-g",  help="genre tag",   action="store_true")
    parser.add_argument("--comment", "-c",  help="comment tag", action="store_true")

    args = parser.parse_args()

    for path in args.file_paths:
        if not os.path.isfile(path):
            parser.error("{0} is not a file.".format(path))

    if not (args.artist or args.album or args.title or args.track or args.year or args.genre or args.comment):
        parser.error("One of --artist, --album, --title, --track, --year, --genre or --comment must be given")
        
    check_artist_tag =  args.artist
    check_album_tag =   args.album
    check_title_tag =   args.title
    check_track_tag =   args.track
    check_year_tag =    args.year 
    check_genre_tag =   args.genre
    check_comment_tag = args.comment

    # READ TAGS ###############################################################

    # For each path specified in command line argmuents
    for path in args.file_paths:

        try:
            file_ref = tagpy.FileRef(path)
            tags = file_ref.tag()

            failed = False

            if check_artist_tag and len(tags.artist.strip()) == 0:
                failed = True

            if check_album_tag and len(tags.album.strip()) == 0:
                failed = True

            if check_title_tag and len(tags.title.strip()) == 0:
                failed = True

            if check_track_tag and tags.track == 0:
                failed = True

            if check_year_tag and tags.year == 0:
                failed = True

            if check_genre_tag and len(tags.genre.strip()) == 0:
                failed = True

            if check_comment_tag and len(tags.comment.strip()) == 0:
                failed = True

            if failed:
                print path

        except ValueError:
            print >> sys.stderr, "Wrong file format:", path

if __name__ == '__main__':
    main()

