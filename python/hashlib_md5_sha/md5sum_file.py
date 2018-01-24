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

import argparse
import hashlib
import os

CHUNK_SIZE = 2**12

def main():
    """Main function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description='Print or check MD5 checksums.')
    parser.add_argument("filepaths", nargs='+', metavar="FILE", help="file to read")
    args = parser.parse_args()

    # COMPUTE HASHS ###########################################################

    for file_path in args.filepaths:
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as fd:
                try:
                    hash_generator = hashlib.md5()
                    #hash_generator = hashlib.sha1()
                    #hash_generator = hashlib.sha256()
                    #hash_generator = hashlib.sha512()

                    data = fd.read(CHUNK_SIZE)
                    while len(data) > 0:
                        hash_generator.update(data)
                        data = fd.read(CHUNK_SIZE)
                except:
                    print("{}: unknown error".format(file_path))  # TODO
                finally:
                    fd.close()

                hash_str = hash_generator.hexdigest()
                print("{}  {}".format(hash_str, file_path))
        else:
            if os.path.isdir(file_path):
                print('"{}" is a directory'.format(file_path))
            else:
                print("unable to read {}".format(file_path))

if __name__ == '__main__':
    main()

