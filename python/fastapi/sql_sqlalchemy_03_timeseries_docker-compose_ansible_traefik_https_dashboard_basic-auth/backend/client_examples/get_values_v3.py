#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# C.f. https://requests.readthedocs.io/en/latest/user/authentication/#basic-authentication

import json
import requests
from config import API_URL, BASIC_AUTH_USER, BASIC_AUTH_PASSWORD

session = requests.Session()
session.auth = (BASIC_AUTH_USER, BASIC_AUTH_PASSWORD)

auth = session.post(API_URL)
res = session.get(f"{API_URL}/values")

# print(res_json)
print(f"HTTP status code: {res.status_code}")

if res.ok:
    res_json = json.loads(res.text)
    print(json.dumps(res_json, indent=4, default=str))
else:
    print(res.reason)
