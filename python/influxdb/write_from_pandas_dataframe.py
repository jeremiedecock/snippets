#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################
# Install the Python client library: pip install influxdb-client
#################################################################

#############################################################################
# Source:                                                                   #
# https://www.influxdata.com/blog/getting-started-with-influxdb-and-pandas/ #
#############################################################################

# REM: THIS SNIPPET SEEMS TO FAIL SILENTLY (NOTHING IS WRITTEN IN INFLUXDB)...

import datetime

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

import pandas as pd

# INITIALIZE THE CLIENT #########################################

with open("INFLUXDB_SECRET_TOKEN", "r") as fd:
    token = fd.read().strip()

org = "jdhp.org"
bucket = "test"

client = InfluxDBClient(url="http://localhost:8086", token=token)

# WRITE DATA ####################################################

# Preparing Dataframe

df = pd.DataFrame([
		    [datetime.datetime.fromisoformat("2020-11-14 22:00:00.000000+00:00"), 23.0, "used_percent2", "mem", "host1"],
		    [datetime.datetime.fromisoformat("2020-11-14 22:00:01.000000+00:00"), 24.0, "used_percent2", "mem", "host1"],
		    [datetime.datetime.fromisoformat("2020-11-14 22:00:02.000000+00:00"), 25.0, "used_percent2", "mem", "host1"],
		  ],
		  columns=["_time", "_value", "_field", "_measurement", "host"])

df.set_index("_time")  # DataFrame must have the timestamp column as an index for the client

print(df)
print(df.dtypes)

# Instanciate the write API

_write_client = client.write_api(write_options=WriteOptions(batch_size=1000,
				                            flush_interval=10_000,
				                            jitter_interval=2_000,
				                            retry_interval=5_000))

_write_client.write(bucket,
	            org=org,
                    record=df,
                    data_frame_measurement_name='cpu',
                    data_frame_tag_columns=['cpu'])

# Close client

_write_client.__del__()
client.__del__()
