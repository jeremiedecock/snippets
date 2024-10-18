#!/usr/bin/env python3

import pyarrow as pa
import pyarrow.parquet as pq

data = {
    'nom': ['Alice', 'Bob', 'Charlie'],
    'âge': [25, 30, 35],
    'salaire': [50000, 60000, 70000]
}

table = pa.Table.from_pydict(data)

pq.write_table(table, 'example_pyarrow.parquet')