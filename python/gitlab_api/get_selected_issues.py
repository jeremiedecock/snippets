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


with open("GITLAB_SECRET_TOKEN", "r") as fd:
    GITLAB_TOKEN = fd.read().strip()

with open("GITLAB_HOST", "r") as fd:
    GITLAB_HOST = fd.read().strip()

HEADER_DICT = {
    "PRIVATE-TOKEN": GITLAB_TOKEN,
    "Content-Type": "application/json",
    "charset": "utf-8"
}

def get_request(get_url):
    """
    https://docs.gitlab.com/ee/api/issues.html

    Parameters
    ----------
    get_url : [type]
        [description]

    Returns
    -------
    [type]
        [description]

    Raises
    ------
    Exception
        [description]
    Exception
        [description]
    Exception
        [description]
    """
    resp = requests.get(get_url, headers=HEADER_DICT)

    json_list = json.loads(resp.text)
    if resp.status_code != 200:
        raise Exception("Error:" + resp.text)
    if resp.encoding.lower() != 'utf-8':
        raise Exception("Encoding error:", resp.encoding)
    if resp.apparent_encoding.lower() != 'utf-8':
        raise Exception("Apparent_encoding error:", resp.apparent_encoding)

    for issue_dict in json_list:
        if ("Ã©" in issue_dict["title"]) or ("â€™" in issue_dict["title"]) or ("Ã‰" in issue_dict["title"]) or ("Ã¢" in issue_dict["title"]): # Ã¨
            print("Encoding err:", issue_dict["id"], issue_dict["web_url"])

    return json_list, resp


def fetch_selected_issues(project_iid_list):
    iid_dict = {}
    for project_id, iid in project_iid_list:
        if project_id not in iid_dict:
            iid_dict[project_id] = []
        iid_dict[project_id].append(iid)

    issue_list = []

    # Group requests per project id
    for project_id, iid_list in iid_dict.items():
        url = GITLAB_HOST + "/api/v4/projects/{}/issues?per_page=100&page={}&scope=all"

        for iid in iid_list:
            url += "&iids[]={}".format(iid)

        json_list, resp = get_request(url.format(project_id, 1))
        issue_list.extend(json_list)

        num_pages = int(resp.headers['X-Total-Pages'])

        for page in range(2, num_pages+1):
            print("page {}/{}".format(page, num_pages))

            json_list, resp = get_request(url.format(project_id, page))
            issue_list.extend(json_list)

    return issue_list


issue_list = fetch_selected_issues(project_iid_list = [(80, 166), (80, 213), (100, 5)])

for issue_dict in issue_list:
    print("{:4d}.{:4d} {}".format(issue_dict["id"], issue_dict["iid"], issue_dict["title"]))