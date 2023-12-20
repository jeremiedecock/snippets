#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

SUBMIT_API_TOKEN = "Dj5XjzKoQjHpsNHgsG1wlpSUZuc6n3hVG5UHOFa6WmdmGHl28PaXC2qY3dkp2bq7"

REQUEST_URL = f"http://127.0.0.1"
HEADER_DICT = {
    "api-token": f"{SUBMIT_API_TOKEN}"
    #"Authorization": f"Bearer {SUBMIT_API_TOKEN}",
    #"Content-Type": "application/json",
}

resp = requests.post(REQUEST_URL, headers=HEADER_DICT)

print(json.dumps(resp.json(), sort_keys=False, indent=4))
