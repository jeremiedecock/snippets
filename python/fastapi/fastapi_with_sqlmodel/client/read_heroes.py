#!/usr/bin/env python3

import os
import requests
from requests.auth import HTTPBasicAuth

VERIFY_SSH_CERTIFICATE = False
USERNAME = os.getenv('HEROES_API_USERNAME')
PASSWORD = os.getenv('HEROES_API_PASSWORD')    # The unencrypted password

r = requests.get(
    'https://api.heroes.jdhp.org/heroes/',
    verify=VERIFY_SSH_CERTIFICATE,
    auth=HTTPBasicAuth(USERNAME, PASSWORD)     # See https://doc.traefik.io/traefik/middlewares/http/basicauth/
)

print(r.text)
