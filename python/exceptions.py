#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# See http://docs.python.org/2/tutorial/errors.html

def foo():
    raise Exception("Error")

def main():
    """Main function"""

    try:
        foo()
    except Exception as e:
        print e


if __name__ == '__main__':
    main()
