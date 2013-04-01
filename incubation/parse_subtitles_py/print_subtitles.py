#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# http://en.wikipedia.org/wiki/SubRip
# http://forum.doom9.org/showthread.php?p=470941#post470941
#
# srt format: 
#    Subtitle number
#    Start time --> End time
#    Text of subtitle (one or more lines)
#    Blank line
#
# The time format used is
#    hours:minutes:seconds,milliseconds

import argparse
import os

LINES_IGNORED = ("www.addic7ed.com\n",
                 "Synced by YYeTs, corrected by gloriabg\n",
                 "Subtitles downloaded from www.OpenSubtitles.org\n",
                 "Sync and corrections by n17t01\n")
WORDS_IGNORED = ("<u>", "<i>", "<b>", "</u>", "</i>", "</b>")

def main():

    # PARSE OPTIONS #######################################

    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('filenames', nargs='+', metavar='FILE', help='file to read')
    args = parser.parse_args()

    # PROCESS FILES #######################################

    for filename in args.filenames:
        print(os.linesep, (8 * "*"), filename, (8 * "*"), os.linesep)

        fd = open(filename)

        read_mode = "srt_number"

        for line in fd.readlines():
            if read_mode == "srt_number":

                # TODO if... else error
                read_mode = "srt_time"

            elif read_mode == "srt_time":

                # TODO if... else error
                read_mode = "srt_text"

            elif line in ("\n", "\r", "\r\n"):

                # TODO if... else error
                read_mode = "srt_number"

            elif line not in LINES_IGNORED:

                for word in line.split():
                    if word not in WORDS_IGNORED:
                        print(word, end=' ')
                print("")

        fd.close()


if __name__ == "__main__":
    main()

