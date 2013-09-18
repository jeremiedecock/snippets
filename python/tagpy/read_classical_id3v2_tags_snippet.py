#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import sys
import tagpy
import tagpy.mpeg

def main():
    """Main function"""

    if(len(sys.argv) == 2):

        _file = tagpy.mpeg.File(sys.argv[1])
        tags = _file.ID3v2Tag()

        frame_dict = {}
        for frame_key in tags.frameListMap().keys():
            frame_list = tags.frameListMap()[frame_key]
            frame_dict[frame_key] = [frame.toString() for frame in frame_list]

        # Print track_number ('TRCK'), composer ('TCOM') and track_title ('TIT2')
        print "{} {} - {}".format(frame_dict['TRCK'][0].split("/")[0], frame_dict['TCOM'][0], frame_dict['TIT2'][0])

if __name__ == '__main__':
    main()

