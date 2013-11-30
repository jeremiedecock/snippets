#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# This is a Python2 module which uses Python3's "print" function (thanks to the "__future__" pseudo module).
# Now "print()" function can be used with Python2.X interpreter.
# The Python2's "print" statement raise an error.
#
# Hopefully, this only concern modules which directly import "__future__".
# Imported modules (like "python2_style_module" here) are not concerned and have to use former "print" statement (otherwise Python2 libraries couldn't be used...).
#
# See: https://larlet.fr/david/blog/2013/python3-future/

from __future__ import print_function

import python2_style_module

def main():
    """Main function"""

    print('This is a python 3 "print()" expression')   # OK
    #print "This is a python 2 print statement"    # ERROR

    python2_style_module.hello()

if __name__ == '__main__':
    main()
