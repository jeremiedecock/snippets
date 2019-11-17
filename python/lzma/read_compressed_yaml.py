#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lzma
import yaml

with lzma.open("test.yaml.xz", "rt") as fd:
    data = yaml.load(fd)

print(data)
