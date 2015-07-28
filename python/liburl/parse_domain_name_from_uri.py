#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# See: https://docs.python.org/3.0/library/urllib.parse.html
#      http://stackoverflow.com/questions/9626535/get-domain-name-from-url

from urllib.parse import urlparse

def main():

    uri = "http://www.jdhp.org/home_en.html"

    parsed_uri = urlparse(uri)
    domain = '{uri.netloc}'.format(uri=parsed_uri)

    print("uri: {}".format(uri))
    print("domain: {}".format(domain))


if __name__ == '__main__':
    main()
