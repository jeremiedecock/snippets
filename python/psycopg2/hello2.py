#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
from secret import DBHOST, DBNAME, DBUSER, DBPASSWORD

# CONNECT TO AN EXISTING DATABASE

conn = psycopg2.connect(
    host=DBHOST,
    database=DBNAME,
    user=DBUSER,
    password=DBPASSWORD,
)


# OPEN A CURSOR TO PERFORM DATABASE OPERATIONS

cur = conn.cursor()


# EXECUTE A COMMAND: THIS CREATES A NEW TABLE

try:
    cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    conn.commit()
except psycopg2.errors.DuplicateTable:
    print("Table already exists, skipping creation.")
    conn.rollback()


# PASS DATA TO FILL A QUERY PLACEHOLDERS AND LET PSYCOPG PERFORM THE CORRECT CONVERSION (NO MORE SQL INJECTIONS!)

cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (1, "abcdef"))
conn.commit()


# QUERY THE DATABASE AND OBTAIN DATA AS PYTHON OBJECTS

cur.execute("SELECT * FROM test;")
res = cur.fetchone()
print(res)


# FETCH ALL RECORDS

cur.execute("SELECT * FROM test;")
res = cur.fetchall()
print(res)


# CURSOR OBJECTS ARE ITERABLE, SO, INSTEAD OF CALLING EXPLICITLY fetchone() IN A LOOP, THE OBJECT ITSELF CAN BE USED (C.F. https://www.psycopg.org/docs/cursor.html)

cur.execute("SELECT * FROM test;")
for record in cur:
    print(record)


# REMOVE ALL RECORDS

cur.execute("DELETE FROM test;")
conn.commit()


# REMOVE THE TABLE
cur.execute("DROP TABLE test;")
conn.commit()


# CLOSE COMMUNICATION WITH THE DATABASE

cur.close()
conn.close()