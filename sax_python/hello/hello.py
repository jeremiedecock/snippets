#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Jérémie DECOCK (http://www.jdhp.org)

import argparse
import xml.sax

from my_handler import MyHandler

def main():
    """Main function"""

    # Parse program arguments
    argparser = argparse.ArgumentParser(description='An argparse snippet.')
    argparser.add_argument('filenames', nargs='+', metavar='FILE', help='file to read')
    args = argparser.parse_args()

    # Make XML parser
    xmlreader = xml.sax.make_parser()
    handler = MyHandler()
    xmlreader.setContentHandler(handler)
    xmlreader.setErrorHandler(handler)

    # Parse XML files
    for filename in args.filenames:
        inputsource = xml.sax.InputSource(filename)
        xmlreader.parse(inputsource)
        #xmlreader.parse(filename)

if __name__ == '__main__':
    main()
