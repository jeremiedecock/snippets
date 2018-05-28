#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml

with open("foo.yaml") as stream:
    data = yaml.safe_load(stream)

print(data)
