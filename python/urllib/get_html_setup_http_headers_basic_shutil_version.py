#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

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

# Warning:
# The urllib2 (from Python 2.x) module has been split across several modules in
# Python 3 named "urllib.request" and "urllib.error".
# Urllib (and thus urllib2) is part of the Python3 standard library but this is
# not the case for urllib3 !
# "urllib and urllib2 have little to do with each other. They were designed to
# be independent and standalone, each solving a different scope of problems,
# and urllib3 follows in a similar vein."

# Online documentation:
# - https://docs.python.org/3/library/urllib.request.html
# - http://stackoverflow.com/questions/24226781/changing-user-agent-in-python-3-for-urrlib-urlopen
# - http://stackoverflow.com/questions/802134/changing-user-agent-on-urllib2-urlopen

import argparse
import shutil
import urllib.request

HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.2.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate'
}

def main():
    """Main function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description='An urllib snippet.')
    parser.add_argument("url", nargs=1, metavar="URL",
                        help="The URL of the webpage to parse.")
    args = parser.parse_args()

    url = args.url[0]
    print("URL:", url)
    print()

    # HTTP REQUEST ############################################################
    # See http://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3

    http_request = urllib.request.Request(url, data=None, headers=HTTP_HEADERS)

    with urllib.request.urlopen(http_request) as http_response, open('out.html', 'wb') as out_file:
        shutil.copyfileobj(http_response, out_file)

if __name__ == '__main__':
    main()

