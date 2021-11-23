#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################
# Install the Python requests library: pip install requests
# http://docs.python-requests.org/en/master/user/quickstart/
#################################################################

# https://docs.gitlab.com/ee/api/issues.html#new-issue

# dict_keys(['id', 'iid', 'project_id', 'title', 'description', 'state', 'created_at', 'updated_at', 'closed_at', 'closed_by', 'labels', 'milestone', 'assignees', 'author', 'type', 'assignee', 'user_notes_count', 'merge_requests_count', 'upvotes', 'downvotes', 'due_date', 'confidential', 'discussion_locked', 'issue_type', 'web_url', 'time_stats', 'task_completion_status', 'blocking_issues_count', 'has_tasks', 'task_status', '_links', 'references', 'moved_to_id', 'service_desk_reply_to'])

import requests
import json
import urllib

PROJECT_ID = 80

def post_request(post_url):
    resp = requests.post(post_url, headers=HEADER_DICT)

    if resp.status_code != 201:
        raise Exception("Error:" + resp.text)

    json_dict = json.loads(resp.text)
    return json_dict


with open("GITLAB_SECRET_TOKEN", "r") as fd:
    GITLAB_TOKEN = fd.read().strip()

with open("GITLAB_HOST", "r") as fd:
    GITLAB_HOST = fd.read().strip()

title = "S0) Test"
title = urllib.parse.quote(title)   # urlencodé

labels = "FT::IA,W::Backlog"
labels = urllib.parse.quote(labels)   # urlencodé

POST_URL = GITLAB_HOST + "/api/v4/projects/{}/issues?title={}&labels={}".format(PROJECT_ID, title, labels)
HEADER_DICT = {"PRIVATE-TOKEN": GITLAB_TOKEN}

json_dict = post_request(POST_URL)
print(json_dict)