#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################
# Install the Python requests library: pip install requests
# http://docs.python-requests.org/en/master/user/quickstart/
#################################################################

# https://developers.notion.com/reference/post-database-query

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
    "page_size": 100
}

def parse_property(property_dict):

    if property_dict["type"] == "rollup":
        value = set()
        for ms in property_dict["rollup"]["array"]:
            for ms2 in ms["multi_select"]:
                value.add(ms2["name"])
        value = list(value)

    elif property_dict["type"] == "multi_select":
        value = set()
        for ms in property_dict["multi_select"]:
            value.add(ms["name"])
        value = list(value)

    elif property_dict["type"] == "select":
        value = None
        if property_dict["select"] is not None:
            value = property_dict["select"]["name"]
    
    elif property_dict["type"] == "rich_text":
        value = ""
        for line in property_dict["rich_text"]:
            value += line['plain_text']
    
    elif property_dict["type"] == "number":
        value =  property_dict["number"]
    
    elif property_dict["type"] == "people":
        value = set()
        for ms in property_dict["people"]:
            value.add(ms["name"])
        value = list(value)
    
    elif property_dict["type"] == "url":
        value =  property_dict["url"]
    
    elif property_dict["type"] == "relation":
        value = set()
        for ms in property_dict["relation"]:
            page_id = ms["id"]
            sub_resp = requests.get(f"https://api.notion.com/v1/pages/{page_id}", headers=HEADER_DICT)

            for k, v in sub_resp.json()["properties"].items():
                if v["type"] == "title":
                    title = ""
                    for line in v["title"]:
                        title += line['plain_text']
                    value.add(title)
        value = list(value)
    
    elif property_dict["type"] == "title":
        value = ""
        for line in property_dict["title"]:
            value += line['plain_text']

    return value


resp = requests.post(REQUEST_URL, headers=HEADER_DICT, data=json.dumps(DATA_DICT))

for row in resp.json()['results']:
    row_dict = {}
    for property, property_dict in row["properties"].items():
        row_dict[property] = parse_property(property_dict)

    print(row_dict)


#with open("db.json", "w") as fd:
#    #json.dump(data, fd)                           # no pretty print
#    json.dump(issue_list, fd, sort_keys=False, indent=4)  # pretty print format