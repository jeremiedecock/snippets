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
        
        tags.artist = "artist test"
        tags.album = "album test"
        tags.title = u"a title with accents éèàç"
        tags.track = 1
        tags.year = 2000
        tags.genre = "genre test"
        tags.comment = u"a comment with accents éèàç"

        file_ref.save()

if __name__ == '__main__':
    main()

