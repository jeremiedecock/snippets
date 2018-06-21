#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml

yaml_str = """---
name: John Smith
age: 33
---
{name: John Foo, age: 34}
"""

for doc in yaml.load_all(yaml_str):
    print(doc)
