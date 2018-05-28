#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml

# Data from http://pyyaml.org/wiki/PyYAML
data = {'name': 'Vorlin Laruknuzum',
        'gold': 423,
        'title': 'Acolyte',
        'hp': [32, 71],
        'sp': [1, 13],
        'sex': 'Male',
        'inventory': ['a Holy Book of Prayers (Words of Wisdom)', 'an Azure Potion of Cure Light Wounds', 'a Siver Wand of Wonder'],
        'class': 'Priest'}

with open("foo.yaml", 'w') as fd:
    yaml.dump(data, fd)
    #yaml.dump(data, fd, default_flow_style=False)
