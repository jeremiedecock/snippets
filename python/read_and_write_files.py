#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Jérémie DECOCK (http://www.jdhp.org)

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
This snippet shows how to read and write files.
"""

#######################################

def write():
    """Write file test."""

    fd = open('foo.txt', 'w')
    fd.write('hello\n')
    fd.write('world\n')
    fd.close()


def write_with_print():
    """Write file test."""

    fd = open('foo.txt', 'w')
    #print >> fd, "Hello"       # Python 2
    print("Hello", file=fd)     # Python 3
    fd.close()


def write_lines():
    """Write file test."""

    words = ['un', 'deux\n', 'trois\n']

    fd = open('foo.txt', 'w')
    fd.writelines(words)
    fd.close()


def write_append():
    """Write file test."""

    fd = open('foo.txt', 'a')
    fd.write('bye\n')
    fd.close()


def write_new_style():
    """Write file test."""

    with open('foo.txt', 'w') as fd:
        fd.write("Hello world")


#######################################


def read_5_bytes():
    """Read file test."""

    fd = open('foo.txt', 'rU')
    text = fd.read(5)
    fd.close()
    print(text)


def read_lines():
    """Read file test."""

    fd = open('foo.txt', 'rU')
    for line in fd.readlines():
        print(line)
    fd.close()


def read_all():
    """Read file test."""

    fd = open('foo.txt', 'rU')
    text = fd.read()
    fd.close()
    print(text)


def read_seek():
    """Read file test."""

    fd = open('foo.txt', 'rU')
    text = fd.read(5)  # Read from byte 0 to 5
    text += fd.read(5)  # Read from byte 5 to 10
    print(text)
    fd.seek(0)         # Go back to the beginning of the file
    text = fd.read(5)  # Read from byte 0 to 5
    print(text)
    fd.close()


def read_new_style():
    """Read file test."""

    with open('foo.txt', 'rU') as fd:
        text = fd.read()

    print(text)

#######################################

if __name__ == '__main__':
    write_lines()
    write_with_print()
    write()
    write_append()
    write_new_style()
    read_5_bytes()
    read_lines()
    read_all()
    read_seek()
    read_new_style()
