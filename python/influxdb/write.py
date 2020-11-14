#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################
# Install the Python client library: pip install influxdb-client
#################################################################

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# INITIALIZE THE CLIENT #########################################

with open("INFLUXDB_SECRET_TOKEN", "r") as fd:
    token = fd.read().strip()

org = "jdhp.org"
bucket = "test"

client = InfluxDBClient(url="http://localhost:8086", token=token)

# WRITE dATA ####################################################

# Option 1: Use InfluxDB Line Protocol to write data

write_api = client.write_api(write_options=SYNCHRONOUS)

data = "mem,host=host1 used_percent=23.43234543"
write_api.write(bucket, org, data)

# Option 2: Use a Data Point to write data

point = Point("mem").tag("host", "host1").field("used_percent", 23.43234543).time(datetime.utcnow(), WritePrecision.NS)
write_api.write(bucket, org, point)

# Option 3: Use a Batch Sequence to write data

sequence = ["mem,host=host1 used_percent=23.43234543",
            "mem,host=host1 available_percent=15.856523"]
write_api.write(bucket, org, sequence)
