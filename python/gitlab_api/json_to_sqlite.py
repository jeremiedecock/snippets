#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
- [x] id
- [x] title
- [x] web_url
- [ ] state
- [ ] description
- [ ] labels
- [ ] updated_at
- [ ] milestone_id
- [ ] type
- [ ] issue_type   ?
- [ ] iid    ?
- [ ] created_at
- [ ] closed_at
- [ ] closed_by
- [ ] assignees_id
- [ ] author_id
- [ ] assignee_id
- [ ] user_notes_count
- [ ] due_date
- [ ] time_stats_time_estimate
- [ ] time_stats_total_time_spent
- [ ] task_completion_status_count
- [ ] task_completion_status_completed_count
- [ ] has_tasks
- [ ] references_full


TABLES DÉDIÉES (?)
- milestones -> milestone_id, milestone_title, milestone_web_url
- users -> id, username
"""

import json
import sqlite3

TABLE_NAME = "issues"

with open("issues.json", "r") as fd:
    issue_list = json.load(fd)

con = sqlite3.connect("issues.sqlite")
cur = con.cursor()

# DELETE TABLE ##############

try:
    cur.execute("DROP TABLE {}".format(TABLE_NAME))
except:
    pass

# CREATE TABLE ##############

sql_query_str = """CREATE TABLE {} (
id       INTEGER,
state    TEXT,
title    TEXT,
web_url  TEXT
)""".format(TABLE_NAME)

cur.execute(sql_query_str)

# FETCH JSON DATA ###########

sql_insert_params = [
    (
        issue_dict["id"],
        issue_dict["state"],
        issue_dict["title"],
        issue_dict["web_url"]
    ) for issue_dict in issue_list
]

# INSERT SQL DATA ###########

cur.executemany("INSERT INTO {} VALUES (?, ?, ?, ?)".format(TABLE_NAME), sql_insert_params)
con.commit()

# PRINT DATA ################

cur.execute("SELECT * FROM issues")
for row in cur:
    print(row)

con.close()