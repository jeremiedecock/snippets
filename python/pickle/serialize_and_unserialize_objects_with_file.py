#!/usr/bin/env python3
# coding: utf-8

import pickle


# Original object ###########

obj1 = [1, 2, 3, 4]

print(obj1)


# Serialized object #########

with open('data.pkl', 'wb') as df:
    pickle.dump(obj1, df)


# Unserialized object #######

with open('data.pkl', 'rb') as df:
    obj2 = pickle.load(df)

print(obj2)
