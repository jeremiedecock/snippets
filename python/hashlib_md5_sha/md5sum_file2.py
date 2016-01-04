#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Return the MD5 hash of a given file.

See https://docs.python.org/3/library/hashlib.html for more information.
"""

import argparse
import hashlib
import os
import sys

# GET THE FILE'S PATH #########################################################

parser = argparse.ArgumentParser(description='A snippet to compute MD5 sums.')

parser.add_argument("file_path_args", nargs=1, metavar="FILE", help="The file to hash")
args = parser.parse_args()
file_path = args.file_path_args[0]

if not os.path.isfile(file_path):
    print(file_path, "is not a valid file.")
    sys.exit(1)

# COMPUTE THE FILE'S HASH #####################################################

# TODO: profile the message digest with different chunk sizes
chunk_size = 2**12

hash_generator = hashlib.md5()
#hash_generator = hashlib.sha1()
#hash_generator = hashlib.sha256()
#hash_generator = hashlib.sha512()

with open(file_path, 'rb') as fd:
    data = fd.read(chunk_size)
    while len(data) > 0:
        hash_generator.update(data)
        data = fd.read(chunk_size)

hash_hex_str = hash_generator.hexdigest()

print(hash_hex_str)

