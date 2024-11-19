#!/usr/bin/env python3

import pyarrow.parquet as pq

table = pq.read_table('example_pyarrow.parquet')

df = table.to_pandas()

print(df)