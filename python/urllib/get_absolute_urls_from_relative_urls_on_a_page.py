#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# Warning:
# Urllib is part of the Python3 standard library but this is not the case for
# urllib2 and urllib3 !
# "urllib and urllib2 have little to do with each other. They were designed to
# be independent and standalone, each solving a different scope of problems,
# and urllib3 follows in a similar vein."

# Online documentation:
# - https://docs.python.org/3.0/library/urllib.parse.html
# - http://stackoverflow.com/questions/9718541/reconstructing-absolute-urls-from-relative-urls-on-a-page

from urllib.parse import urljoin

def main():

    base = "http://www.jdhp.org/foo/bar/baz.html"
    relative_url = "../../images/img.png"

    absolute_url = urljoin(base, relative_url)

    print(absolute_url)


if __name__ == '__main__':
    main()
