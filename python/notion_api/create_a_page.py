#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################
# Install the Python requests library: pip install requests
# http://docs.python-requests.org/en/master/user/quickstart/
#################################################################

# Src: https://developers.notion.com/reference/post-page

import requests
import json

with open("NOTION_SECRET_TOKEN", "r") as fd:
    NOTION_TOKEN = fd.read().strip()

with open("NOTION_DB_ID", "r") as fd:
    NOTION_DB_ID = fd.read().strip()


REQUEST_URL = f"https://api.notion.com/v1/pages"
HEADER_DICT = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}

DATA_DICT = {
    "parent": {
        "database_id": NOTION_DB_ID
    },
    "properties": {
        "Photo": {
            "url": "www.google.fr"
        },
        "Score": {
            "rich_text": [
                {
					"text": {
						"content": "Yep"
					}
				}
            ]
        },
        "Author": {
            "rich_text": [
                {
					"text": {
						"content": "Yep"
					}
				}    
            ]
        },
        "Store availability": {
            "multi_select": [
                {
                    "name": "B"
                },
                {
                    "name": "C"
                }
            ]
        },
        "Book Title": {
            "title": [
                {
					"text": {
						"content": "Yakari"
					}
				}
            ]
        }
    }
}

resp = requests.post(REQUEST_URL, headers=HEADER_DICT, data=json.dumps(DATA_DICT))

print(json.dumps(resp.json(), sort_keys=False, indent=4))

#with open("db.json", "w") as fd:
#    #json.dump(data, fd)                           # no pretty print
#    json.dump(issue_list, fd, sort_keys=False, indent=4)  # pretty print format