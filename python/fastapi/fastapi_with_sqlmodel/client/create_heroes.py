#!/usr/bin/env python3

import os
import requests
from requests.auth import HTTPBasicAuth

VERIFY_SSH_CERTIFICATE = False
USERNAME = os.getenv('HEROES_API_USERNAME')
PASSWORD = os.getenv('HEROES_API_PASSWORD')    # The unencrypted password

payload = {
  "name": "Iron Man",
  "secret_name": "Bob",
  "age": 20
}

# RAW DATA

# r = requests.post(
#     "https://api.heroes.jdhp.org/heroes/",
#     data=payload,
#     verify=VERIFY_SSH_CERTIFICATE,
#     auth=HTTPBasicAuth(USERNAME, PASSWORD)     # See https://doc.traefik.io/traefik/middlewares/http/basicauth/
# )

# print(r.text)

# JSON DATA

r = requests.post(
    "https://api.heroes.jdhp.org/heroes/",
    json=payload,
    verify=VERIFY_SSH_CERTIFICATE,
    auth=HTTPBasicAuth(USERNAME, PASSWORD)     # See https://doc.traefik.io/traefik/middlewares/http/basicauth/
)

print(r.text)
