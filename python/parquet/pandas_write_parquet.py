#!/usr/bin/env python3

import pandas as pd

data = {
    'nom': ['Alice', 'Bob', 'Charlie'],
    'âge': [25, 30, 35],
    'salaire': [50000, 60000, 70000]
}
df = pd.DataFrame(data)

df.to_parquet('example_pandas.parquet')