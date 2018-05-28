#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml

# Data from http://pyyaml.org/wiki/PyYAML
yaml_str = """
name: Vorlin Laruknuzum
sex: Male
class: Priest
title: Acolyte
hp: [32, 71]
sp: [1, 13]
gold: 423
inventory:
- a Holy Book of Prayers (Words of Wisdom)
- an Azure Potion of Cure Light Wounds
- a Silver Wand of Wonder
"""

data = yaml.load(yaml_str)

print(data)
