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

"""
This snippet test Python properties.

See: https://docs.python.org/3/library/functions.html#property
"""

class Foo(object):

    def __init__(self):
        self._x = None

    @property
    def x(self):
        """The 'x' property docstring."""
        print('get_x')
        return self._x

    @x.setter
    def x(self, value):
        print('set_x: ', value)
        self._x = value

    @x.deleter
    def x(self):
        print('del_x')
        del self._x


def main():
    """Main function"""

    foo = Foo() 
    print(foo.x)
    print()

    foo.x = 3
    print(foo.x)
    print()

    del foo.x
    foo.x = 3
    print(foo.x)
    print()
    
    print(Foo.x.__doc__)
    print()

    foo._x = 4
    print(foo.x)

if __name__ == '__main__':
    main()
