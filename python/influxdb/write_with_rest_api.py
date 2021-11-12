#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################
# Install the Python requests library: pip install requests
# http://docs.python-requests.org/en/master/user/quickstart/
#################################################################

from datetime import datetime

import requests
import time

with open("INFLUXDB_SECRET_TOKEN", "r") as fd:
    INFLUXDB_TOKEN = fd.read().strip()

INFLUXDB_BUCKET = "test"
POST_URL = "http://localhost:8086/api/v2/write?org=jdhp.org&bucket={}&precision=s".format(INFLUXDB_BUCKET)
HEADER_DICT = {"Authorization": "Token {}".format(INFLUXDB_TOKEN)}

# WRITE DATA ####################################################

data_str = "mem,host=host1 used_percent=70.0"
resp = requests.post(POST_URL, data=data_str, headers=HEADER_DICT)

if resp.status_code != 204:
    print("Error:", resp.text)
