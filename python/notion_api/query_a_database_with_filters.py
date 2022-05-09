#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################
# Install the Python requests library: pip install requests
# http://docs.python-requests.org/en/master/user/quickstart/
#################################################################

# https://developers.notion.com/reference/post-database-query

import requests
import json
import common as notionapi

with open("NOTION_SECRET_TOKEN", "r") as fd:
    NOTION_TOKEN = fd.read().strip()

with open("NOTION_DB_ID", "r") as fd:
    NOTION_DB_ID = fd.read().strip()


REQUEST_URL = f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query"
HEADER_DICT = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

DATA_DICT = {
    "filter": {
        "property": "Store availability",
        "multi_select": {
            "contains": "B"
        }
    }
}


resp = requests.post(REQUEST_URL, headers=HEADER_DICT, data=json.dumps(DATA_DICT))

print(json.dumps(resp.json(), sort_keys=False, indent=4))

for row in resp.json()['results']:
    row_dict = {
        "page_id": row["id"]
    }

    for property, property_dict in row["properties"].items():
        row_dict[property] = notionapi.parse_property(property_dict)

    print(row_dict)


#with open("db.json", "w") as fd:
#    #json.dump(data, fd)                           # no pretty print
#    json.dump(issue_list, fd, sort_keys=False, indent=4)  # pretty print format