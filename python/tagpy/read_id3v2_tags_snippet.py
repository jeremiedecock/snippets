#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import sys
import tagpy
import tagpy.mpeg

def main():
    """Main function"""

    if(len(sys.argv) == 2):

        print 3*'*', sys.argv[1], 3*'*'
        print 

        _file = tagpy.mpeg.File(sys.argv[1])
        tags = _file.ID3v2Tag()

        for frame_key in tags.frameListMap().keys():
            print frame_key
            frame_list = tags.frameListMap()[frame_key]
            for frame in frame_list:
                print "   %s" % frame.toString()

if __name__ == '__main__':
    main()

