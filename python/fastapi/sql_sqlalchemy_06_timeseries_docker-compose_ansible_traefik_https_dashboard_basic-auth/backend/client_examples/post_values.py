#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)

SUBMIT_API_TOKEN = ""
SUBMIT_API_URL = ""

PARTICIPANT_ID = 99999 # random.randint(1, 5)
TEAM_ID = 99999 #  random.randint(1, 5)
SUBMISSION_ID = 99998 # random.randint(1, 1000)

payload = {
    "api-token": SUBMIT_API_TOKEN,
    "challenge-id": 82,
    #"git-url": "https://gitlab.com/ens-data-challenge/accenta-rl-agent-example",
    #"git-url": "https://gitlab.com/arnaud.gardille/accenta-rl-agent-example",
    "git-url": "https://gitlab.com/ens-data-challenge/arnaud-gardille-rl-agent",
    "git-token": "my_secret_token",
    "participant-id": PARTICIPANT_ID,
    "team-id": TEAM_ID,
    "submission-id": SUBMISSION_ID
}

res = requests.post(f"{SUBMIT_API_URL}/submissions", data=payload, verify=SSL_CRT_PATH)

res_json = json.loads(res.text)
print(f"HTTP status code: {res.status_code}")
print(json.dumps(res_json, indent=4, default=str))
