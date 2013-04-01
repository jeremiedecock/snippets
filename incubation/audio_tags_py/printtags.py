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

DESCRIPTION = "A very basig snippet to read ID3, OGG, ... tags with TagPy (a taglib binding)."
EPILOG = "Please report bugs to <jd.jdhp@gmail.com>."
VERSION = "1.0"

def main():
    """Main function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument("file_paths", nargs='+', metavar="FILE", help="file to scan")
    args = parser.parse_args()

    for path in args.file_paths:
        if not os.path.isfile(path):
            print "ERROR: {0} is not a file.".format(path)
            print parser.format_usage(),
            sys.exit(2)

    # READ TAGS ###############################################################

    # For each path specified in command line argmuents
    for path in args.file_paths:

        print 
        print 3*'*', path, 3*'*'
        print 

        try:
            file_ref = tagpy.FileRef(path)
            tags = file_ref.tag()
            
            print u'artist      : "{0}"'.format(tags.artist)
            print u'album       : "{0}"'.format(tags.album)
            print u'title       : "{0}"'.format(tags.title)
            print  'track       : {0}'.format(tags.track)
            print  'year        : {0}'.format(tags.year)
            print u'genre       : "{0}"'.format(tags.genre)
            print u'comment     : "{0}"'.format(tags.comment)

            audio_properties = file_ref.audioProperties()

            seconds = audio_properties.length % 60
            minutes = (audio_properties.length - seconds) / 60;

            print 'length      : {0}:{1}'.format(minutes, seconds)
            print 'bitrate     : {0}'.format(audio_properties.bitrate)
            print 'sample rate : {0}'.format(audio_properties.sampleRate)
            print 'channels    : {0}'.format(audio_properties.channels)

        except ValueError as ex:
            print >> sys.stderr, "Wrong file format:", path

if __name__ == '__main__':
    main()

