#!/usr/bin/env python
# -*- coding: utf-8 -*-

import objgraph

foo = {}
foo['A'] = 1
foo['B'] = 2

objgraph.show_refs([foo], filename='foo.png')
