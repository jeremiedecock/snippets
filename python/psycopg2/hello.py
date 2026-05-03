#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
from secret import DBHOST, DBNAME, DBUSER, DBPASSWORD

conn = psycopg2.connect(
    host=DBHOST,
    database=DBNAME,
    user=DBUSER,
    password=DBPASSWORD,
)

cur = conn.cursor()
cur.execute("SELECT version();")
print(cur.fetchone())

cur.close()
conn.close()