#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2 import sql
from secret import DBHOST, DBNAME, DBUSER, DBPASSWORD

TABLE_NAME = "hello3"


# CONNECT TO AN EXISTING DATABASE

conn = psycopg2.connect(
    host=DBHOST,
    database=DBNAME,
    user=DBUSER,
    password=DBPASSWORD,
)


# OPEN A CURSOR TO PERFORM DATABASE OPERATIONS

cur = conn.cursor()


###########################################################################
# TABLE IDENTIFIERS USE sql.Identifier TO PREVENT SQL INJECTION.          #
# LITERAL VALUES USE PSYCOPG2 %s PLACEHOLDERS.                            #
###########################################################################


# EXECUTE A COMMAND: THIS CREATES A NEW TABLE
# - id         : randomly generated UUID (gen_random_uuid(), native PostgreSQL 13+)
# - created_at : timezone-aware timestamp (TIMESTAMPTZ)

try:
    cur.execute(
        sql.SQL(
            "CREATE TABLE {} ("
            "  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), "
            "  created_at timestamptz NOT NULL DEFAULT NOW()"
            ");"
        ).format(sql.Identifier(TABLE_NAME))
    )
    conn.commit()
except psycopg2.errors.DuplicateTable:
    print("Table already exists, skipping creation.")
    conn.rollback()


# INSERT DATA INTO THE TABLE
# Both columns have default values, so DEFAULT VALUES is used.

cur.execute(
    sql.SQL("INSERT INTO {} DEFAULT VALUES;").format(sql.Identifier(TABLE_NAME))
)
conn.commit()


# QUERY THE DATABASE AND OBTAIN DATA AS PYTHON OBJECTS

cur.execute(sql.SQL("SELECT * FROM {};").format(sql.Identifier(TABLE_NAME)))
res = cur.fetchall()
print(res)


# CLOSE COMMUNICATION WITH THE DATABASE

cur.close()
conn.close()