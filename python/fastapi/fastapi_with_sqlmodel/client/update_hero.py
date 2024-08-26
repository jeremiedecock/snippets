#!/usr/bin/env python3

import json
import os
import requests
from requests.auth import HTTPBasicAuth

VERIFY_SSH_CERTIFICATE = True
USERNAME = os.getenv('HEROES_API_USERNAME')
PASSWORD = os.getenv('HEROES_API_PASSWORD')    # The unencrypted password

HERO_ID = 2

payload = {
  "name": "Spider-Boy",
  "secret_name": "Pedro Parqueador",
  "age": 16
}

# JSON DATA

r = requests.put(
    f'https://heroes.jdhp.org/api/{HERO_ID}',
    params={'hero_id': HERO_ID},
    json=payload,
    verify=VERIFY_SSH_CERTIFICATE,
    auth=HTTPBasicAuth(USERNAME, PASSWORD)     # See https://doc.traefik.io/traefik/middlewares/http/basicauth/
)

# print(r.text)                        # r.text return a (JSON) string
# print(r.json())                      # r.json() return a Python structure (dict, list, etc.)
print(json.dumps(r.json(), indent=4))  # More readable...
