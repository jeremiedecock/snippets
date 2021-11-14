#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################
# Install the Python requests library: pip install requests
# http://docs.python-requests.org/en/master/user/quickstart/
#################################################################

# https://docs.gitlab.com/ee/api/index.html#personalproject-access-tokens

# dict_keys(['id', 'iid', 'project_id', 'title', 'description', 'state', 'created_at', 'updated_at', 'closed_at', 'closed_by', 'labels', 'milestone', 'assignees', 'author', 'type', 'assignee', 'user_notes_count', 'merge_requests_count', 'upvotes', 'downvotes', 'due_date', 'confidential', 'discussion_locked', 'issue_type', 'web_url', 'time_stats', 'task_completion_status', 'blocking_issues_count', 'has_tasks', 'task_status', '_links', 'references', 'moved_to_id', 'service_desk_reply_to'])

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

GET_URL = GITLAB_HOST + "/api/v4/issues?per_page=100&page=1&scope=all"
HEADER_DICT = {"PRIVATE-TOKEN": GITLAB_TOKEN}

issue_list = []

json_list, resp = get_request(GET_URL)
num_pages = int(resp.headers['X-Total-Pages'])

for page in range(2, num_pages+1):
    #print(".", end="", flush=True)
    print("page {}/{}".format(page, num_pages))
    issue_list.extend(json_list)
    next_page = GITLAB_HOST + "/api/v4/issues?per_page=100&page={}&scope=all".format(page)
    json_list, resp = get_request(next_page)

    with open("issues.json", "w") as fd:
        #json.dump(data, fd)                           # no pretty print
        json.dump(issue_list, fd, sort_keys=False, indent=4)  # pretty print format

#print(group_list[0].keys())




for issue_dict in issue_list:
    print("{:4d}. {}".format(issue_dict["id"], issue_dict["title"]))