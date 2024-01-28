#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import API_URL, API_TOKEN
import datetime
import json
import random
import requests

headers = {"api-token": API_TOKEN}

payload = {
    "name": "temperature",
    "datetime": datetime.datetime.now().isoformat(),
    "value": random.normalvariate(20, 5)
}

res = requests.post(f"{API_URL}/values", json=payload, headers=headers)

# print(res_json)
print(f"HTTP status code: {res.status_code}")

if res.ok:
    res_json = json.loads(res.text)
    print(json.dumps(res_json, indent=4, default=str))
else:
    print(res.reason)
