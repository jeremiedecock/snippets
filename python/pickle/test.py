#!/usr/bin/env python
# coding: utf-8

import pickle

obj = {'hello':1, 'world':2}

print obj

str_obj = pickle.dumps(obj)

print str_obj

obj = pickle.loads(str_obj)

print obj
