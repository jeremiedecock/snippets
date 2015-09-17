#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# Warning:
# The urllib2 (from Python 2.x) module has been split across several modules in
# Python 3 named "urllib.request" and "urllib.error".
# Urllib (and thus urllib2) is part of the Python3 standard library but this is
# not the case for urllib3 !
# "urllib and urllib2 have little to do with each other. They were designed to
# be independent and standalone, each solving a different scope of problems,
# and urllib3 follows in a similar vein."

# Online documentation:
# - https://docs.python.org/3.0/library/urllib.parse.html
# - http://stackoverflow.com/questions/9626535/get-domain-name-from-url

from urllib.parse import urlparse

def main():

    uri = "http://www.jdhp.org/home_en.html"

    parsed_uri = urlparse(uri)

    print("uri", uri)
    print(parsed_uri)

    print("scheme",   parsed_uri.scheme)
    print("netloc",   parsed_uri.netloc)
    print("path",     parsed_uri.path)
    print("params",   parsed_uri.params)
    print("query",    parsed_uri.query)
    print("fragment", parsed_uri.fragment)
    print("username", parsed_uri.username)
    print("password", parsed_uri.password)
    print("hostname", parsed_uri.hostname)
    print("port",     parsed_uri.port)


if __name__ == '__main__':
    main()
