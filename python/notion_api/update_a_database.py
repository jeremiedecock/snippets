#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################
# Install the Python requests library: pip install requests
# http://docs.python-requests.org/en/master/user/quickstart/
#################################################################

# https://developers.notion.com/reference/update-a-database

import requests
import json

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
    # title (array):
    # Title of database as it appears in Notion.
    # An array of rich text objects.
    # If omitted, the database title will remain unchanged.
    "title": [
        {
            "text": {
                "content": "Book Title"
            }
        }
    ],

    # properties (json):
    # Updates to the property schema of a database.
    # If updating an existing property, the keys are the names or IDs of the properties as they appear in Notion and the values are property schema objects.
    # If adding a new property, the key is the name of the database property and the value is a property schema object.
    "properties": {

        # Add or redefine the "Photo" property schema
        "Photo": {
            "url": {}
        },

        # Add or redefine the "Store availability" property schema
        "Store availability": {
            "multi_select": {
                "options": [
                    {
                        "name": "Duc Loi Market"
                    },
                    {
                        "name": "Rainbow Grocery"
                    },
                    {
                        "name": "Gus'\''s Community Market"
                    },
                    {
                        "name": "The Good Life Grocery",
                        "color": "orange"
                    }
                ]
            }
        }
    }  
}


resp = requests.patch(REQUEST_URL, headers=HEADER_DICT, data=json.dumps(DATA_DICT))

print(json.dumps(resp.json(), sort_keys=False, indent=4))
