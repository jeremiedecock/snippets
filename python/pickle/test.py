#!/usr/bin/env python3
# coding: utf-8

import pickle


# Original object ###########

obj = {'hello':1, 'world':2}

print(obj)


# Serialized object #########

str_obj = pickle.dumps(obj)

print(str_obj)


# Unserialized object #######

obj = pickle.loads(str_obj)

print(obj)
