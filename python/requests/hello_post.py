#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

payload = {'key1': 'value1', 'key2': 'value2'}

# RAW DATA

r = requests.post("https://httpbin.org/post", data=payload)

print(r.text)

# JSON DATA

r = requests.post("https://httpbin.org/post", json=payload)

print(r.text)
