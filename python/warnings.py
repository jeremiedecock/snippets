#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Jérémie DECOCK (http://www.jdhp.org)

import warnings

def custom_formatwarning(message, category, filename, lineno, line=""):
    """Ignore everything except the message."""
    return "Warning: " + str(message) + "\n"

def main():
    """Main function"""

    warnings.formatwarning = custom_formatwarning

    warnings.warn("Foo", UserWarning)


if __name__ == '__main__':
    main()

