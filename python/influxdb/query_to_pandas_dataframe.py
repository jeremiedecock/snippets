#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################
# Install the Python client library: pip install influxdb-client
#################################################################

#############################################################################
# Source:                                                                   #
# https://www.influxdata.com/blog/getting-started-with-influxdb-and-pandas/ #
#############################################################################

from influxdb_client import InfluxDBClient
import pandas as pd

# INITIALIZE THE CLIENT #########################################

with open("INFLUXDB_SECRET_TOKEN", "r") as fd:
    token = fd.read().strip()

org = "jdhp.org"
bucket = "test"

client = InfluxDBClient(url="http://localhost:8086", token=token)

# READ DATA #####################################################

# Execute a Flux query

query = f'from(bucket: "' + bucket + f'") |> range(start: -1h)'
df = client.query_api().query_data_frame(query=query, org=org)
print(df.head())
