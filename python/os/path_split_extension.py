#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

file_path = '/path/to/somefile.ext'

file_name, file_extension = os.path.splitext(file_path)

print("File path:", file_path)
print("File name:", file_name)
print("File extension:", file_extension)
