#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################
# Install the Python requests library: pip install requests
# http://docs.python-requests.org/en/master/user/quickstart/
#################################################################

# Src: https://developers.notion.com/reference/retrieve-a-database

import requests
import json

with open("NOTION_SECRET_TOKEN", "r") as fd:
    NOTION_TOKEN = fd.read().strip()

with open("NOTION_PAGE_ID", "r") as fd:
    NOTION_PAGE_ID = fd.read().strip()


REQUEST_URL = f"https://api.notion.com/v1/pages/{NOTION_PAGE_ID}"
HEADER_DICT = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}

resp = requests.get(REQUEST_URL, headers=HEADER_DICT)

print(json.dumps(resp.json(), sort_keys=False, indent=4))

#with open("db.json", "w") as fd:
#    #json.dump(data, fd)                           # no pretty print
#    json.dump(issue_list, fd, sort_keys=False, indent=4)  # pretty print format