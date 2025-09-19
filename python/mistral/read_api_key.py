#!/usr/bin/env python3

import tomllib

with open("secrets.toml", "rb") as f:
    data = tomllib.load(f)

print(data['mistral_api_key'])
