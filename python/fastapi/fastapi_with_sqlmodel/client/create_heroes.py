#!/usr/bin/env python3

import json
import os
import requests
from requests.auth import HTTPBasicAuth

VERIFY_SSH_CERTIFICATE = True
USERNAME = os.getenv('HEROES_API_USERNAME')
PASSWORD = os.getenv('HEROES_API_PASSWORD')    # The unencrypted password


# HERO 1

payload = {
  "name": "Rusty-Man",
  "secret_name": "Tommy Sharp",
  "age": 48
}

r = requests.post(
    "https://heroes.jdhp.org/api/",
    json=payload,
    verify=VERIFY_SSH_CERTIFICATE,
    auth=HTTPBasicAuth(USERNAME, PASSWORD)     # See https://doc.traefik.io/traefik/middlewares/http/basicauth/
)

# print(r.text)                        # r.text return a (JSON) string
# print(r.json())                      # r.json() return a Python structure (dict, list, etc.)
print(json.dumps(r.json(), indent=4))  # More readable...


# HERO 2

payload = {
  "name": "Captain North America",
  "secret_name": "Esteban Rogelios",
  "age": 93
}

r = requests.post(
    "https://heroes.jdhp.org/api/",
    json=payload,
    verify=VERIFY_SSH_CERTIFICATE,
    auth=HTTPBasicAuth(USERNAME, PASSWORD)     # See https://doc.traefik.io/traefik/middlewares/http/basicauth/
)


# print(r.text)                        # r.text return a (JSON) string
# print(r.json())                      # r.json() return a Python structure (dict, list, etc.)
print(json.dumps(r.json(), indent=4))  # More readable...
