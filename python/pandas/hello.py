#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: http://pandas.pydata.org/pandas-docs/stable/10min.html#min

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create a "Series"
s = pd.Series([1, 3, 5, np.nan, 6, 8])
print(s)
print()

# Create a "DataFrame"
dates = pd.date_range('20130101', periods=6)
print(dates)
print()

df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
print(df)
print()

print(df.dtypes)
print()

