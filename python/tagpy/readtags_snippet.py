#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import sys
import tagpy

def main():
    """Main function"""

    if(len(sys.argv) == 2):

        print 3*'*', sys.argv[1], 3*'*'
        print 

        file_ref = tagpy.FileRef(sys.argv[1])
        tags = file_ref.tag()
        
        print "artist      :", tags.artist
        print "album       :", tags.album
        print "title       :", tags.title
        print "track       :", tags.track
        print "year        :", tags.year
        print "genre       :", tags.genre
        print "comment     :", tags.comment

        audio_properties = file_ref.audioProperties()

        print "length      :", audio_properties.length
        print "bitrate     :", audio_properties.bitrate
        print "sample rate :", audio_properties.sampleRate
        print "channels    :", audio_properties.channels

if __name__ == '__main__':
    main()

