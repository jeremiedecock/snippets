#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml

with open("foo.yaml") as stream:
    data = yaml.load(stream)

print(data)
