#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################
# Install the Python requests library: pip install requests
# http://docs.python-requests.org/en/master/user/quickstart/
#################################################################

# https://docs.gitlab.com/ee/api/index.html#personalproject-access-tokens

import requests
import json

def get_request(get_url):
    resp = requests.get(get_url, headers=HEADER_DICT)

    json_list = json.loads(resp.text)
    if resp.status_code != 200:
        raise Exception("Error:" + resp.text)

    return json_list, resp


with open("GITLAB_SECRET_TOKEN", "r") as fd:
    GITLAB_TOKEN = fd.read().strip()

with open("GITLAB_HOST", "r") as fd:
    GITLAB_HOST = fd.read().strip()

GET_URL = GITLAB_HOST + "/api/v4/projects?pagination=keyset&per_page=50&order_by=id&sort=asc"
HEADER_DICT = {"PRIVATE-TOKEN": GITLAB_TOKEN}

project_list = []

json_list, resp = get_request(GET_URL)

while "Link" in resp.headers:
    print(".", end="", flush=True)
    next_page = resp.headers["Link"][1:].split(">")[0]
    project_list.extend(json_list)
    json_list, resp = get_request(next_page)

print(project_list[0].keys())

for project_dict in project_list:
    print("{:3d}. {}".format(project_dict["id"], project_dict["path_with_namespace"]))