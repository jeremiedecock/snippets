#!/usr/bin/env python3

"""
Client script to test the FastAPI authentication endpoint.

Usage:
    python client.py
"""

import requests

URL = "http://127.0.0.1:8000/api/counter"
TOKEN = "token_abc123"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TOKEN}",
}

response = requests.get(URL, headers=headers)

print(f"Status code: {response.status_code}")
print(f"Response: {response.json()}")
