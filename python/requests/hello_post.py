#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

payload = {'key1': 'value1', 'key2': 'value2'}

r = requests.post("https://httpbin.org/post", data=payload)

print(r.text)
