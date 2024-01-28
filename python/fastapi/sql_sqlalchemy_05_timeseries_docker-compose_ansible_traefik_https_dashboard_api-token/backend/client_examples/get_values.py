#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# C.f. https://requests.readthedocs.io/en/latest/user/authentication/#basic-authentication

from config import API_URL, API_TOKEN
import json
import requests

headers = {"api-token": API_TOKEN}

res = requests.get(f"{API_URL}/values", headers=headers)

# print(res_json)
print(f"HTTP status code: {res.status_code}")

if res.ok:
    res_json = json.loads(res.text)
    print(json.dumps(res_json, indent=4, default=str))
else:
    print(res.reason)
