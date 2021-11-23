#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################
# Install the Python requests library: pip install requests
# http://docs.python-requests.org/en/master/user/quickstart/
#################################################################

# TODO:
# - AJOUTER UNE CLÉ PRIMAIRE SUR ID
# - AJOUTER UNE COLONNE CREATED_AT

# https://docs.gitlab.com/ee/api/index.html#personalproject-access-tokens

# dict_keys(['id', 'iid', 'project_id', 'title', 'description', 'state', 'created_at', 'updated_at', 'closed_at', 'closed_by', 'labels', 'milestone', 'assignees', 'author', 'type', 'assignee', 'user_notes_count', 'merge_requests_count', 'upvotes', 'downvotes', 'due_date', 'confidential', 'discussion_locked', 'issue_type', 'web_url', 'time_stats', 'task_completion_status', 'blocking_issues_count', 'has_tasks', 'task_status', '_links', 'references', 'moved_to_id', 'service_desk_reply_to'])

import requests
import json
import sqlite3
import datetime

TABLE_NAME = "issues"

with open("GITLAB_SECRET_TOKEN", "r") as fd:
    GITLAB_TOKEN = fd.read().strip()

with open("GITLAB_HOST", "r") as fd:
    GITLAB_HOST = fd.read().strip()

HEADER_DICT = {"PRIVATE-TOKEN": GITLAB_TOKEN}


def str_to_datetime(datetime_str):
    """e.g. : 2021-11-16T16:07:05.688Z -> 2021-11-16T16:07:05.688+00:00"""
    return datetime.datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))


def get_request(get_url):
    resp = requests.get(get_url, headers=HEADER_DICT)

    json_list = json.loads(resp.text)
    if resp.status_code != 200:
        raise Exception("Error:" + resp.text)

    return json_list, resp


def fetch_issues(update_after=None):
    issue_list = []

    params_str = "updated_after={},".format(update_after) if update_after is not None else ""

    json_list, resp = get_request(GITLAB_HOST + "/api/v4/issues?{}per_page=100&page=1&scope=all".format(params_str))
    num_pages = int(resp.headers['X-Total-Pages'])

    for page in range(2, num_pages+1):
        print("page {}/{}".format(page, num_pages))
        issue_list.extend(json_list)
        next_page = GITLAB_HOST + "/api/v4/issues?{}per_page=100&page={}&scope=all".format(params_str, page)
        json_list, resp = get_request(next_page)

    return issue_list


def make_sqlite_database(issue_list):
    con = sqlite3.connect("issues.sqlite")
    cur = con.cursor()

    # DELETE TABLE ##############

    try:
        cur.execute("DROP TABLE {}".format(TABLE_NAME))
    except:
        pass

    # CREATE TABLE ##############

    sql_query_str = """CREATE TABLE {} (
        id               INTEGER,
        state            TEXT,
        title            TEXT,
        description      TEXT,
        labels           TEXT,
        created_at       TEXT,
        updated_at       TEXT,
        milestone_id     INTEGER,
        web_url          TEXT,
        project_id       INTEGER,
        iid              INTEGER,
        upload_required  INTEGER,
        PRIMARY KEY (id)
    )""".format(TABLE_NAME)

    cur.execute(sql_query_str)

    # FETCH JSON DATA ###########

    sql_insert_params = [
            (
                issue_dict["id"],
                issue_dict["state"],
                issue_dict["title"],
                issue_dict["description"],
                ",".join(issue_dict["labels"]),
                issue_dict["created_at"],
                issue_dict["updated_at"],
                #issue_dict["milestone"]["id"] if ("milestone" in issue_dict and "id" in issue_dict["milestone"]) else "",
                issue_dict["milestone"]["id"] if (issue_dict["milestone"] is not None) else "",
                issue_dict["web_url"],
                issue_dict["project_id"],
                issue_dict["iid"],
                0,
                ) for issue_dict in issue_list
            ]

    # INSERT SQL DATA ###########

    question_marks = ", ".join(["?" for x in sql_insert_params[0]])
    query_str = "INSERT INTO {} VALUES ({})".format(TABLE_NAME, question_marks)
    cur.executemany(query_str, sql_insert_params)
    con.commit()
    con.close()



issue_list = fetch_issues()
make_sqlite_database(issue_list)
