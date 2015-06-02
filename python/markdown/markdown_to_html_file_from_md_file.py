#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
This is the simplest Python3 markdown converter snippet.

WARNING: Debian users have to install the "python3-markdown" package to run
         this snippet.

SEE: /usr/share/doc/python-markdown-doc/docs/index.html ("python-markdown-doc" Debian package)
"""

import markdown

def main():
    # Available output formats are:
    # - "xhtml1": Outputs XHTML 1.x. Default.
    # - "xhtml5": Outputs XHTML style tags of HTML 5
    # - "xhtml": Outputs latest supported version of XHTML (currently XHTML 1.1).
    # - "html4": Outputs HTML 4
    # - "html5": Outputs HTML style tags of HTML 5
    # - "html": Outputs latest supported version of HTML (currently HTML 4).
    markdown.markdownFromFile(input="test.md", output="test.html", output_format="html5")

if __name__ == '__main__':
    main()
