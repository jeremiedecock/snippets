#!/usr/bin/env python3
# coding: utf-8

import pickle
import numpy as np
from astropy import units as u
import pandas as pd


# Original object ###########

obj1 = [np.random.random(size=3), 3. * u.meter, pd.DataFrame([1., 2., np.nan], columns=["Val"])]

print(obj1)


# Serialized object #########

with open('data.pkl', 'wb') as df:
    pickle.dump(obj1, df)


# Unserialized object #######

with open('data.pkl', 'rb') as df:
    obj2 = pickle.load(df)

print(obj2)
