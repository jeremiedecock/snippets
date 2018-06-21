#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml

data_list = [{'name': 'John Smith', 'age': 33},
             {'name': 'John Foo', 'age': 34}]     # it can be any sequence or iterable

yaml_str = yaml.dump_all(data_list, default_flow_style=False)
print(yaml_str)
