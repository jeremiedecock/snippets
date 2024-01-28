#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# C.f. https://requests.readthedocs.io/en/latest/user/authentication/#basic-authentication

import json
import requests
from requests.auth import HTTPBasicAuth
from config import API_URL, BASIC_AUTH_USER, BASIC_AUTH_PASSWORD

basic = HTTPBasicAuth(BASIC_AUTH_USER, BASIC_AUTH_PASSWORD)

res = requests.get(f"{API_URL}/values", auth=basic)

# print(res_json)
print(f"HTTP status code: {res.status_code}")

if res.ok:
    res_json = json.loads(res.text)
    print(json.dumps(res_json, indent=4, default=str))
else:
    print(res.reason)
