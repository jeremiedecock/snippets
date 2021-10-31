#!/usr/bin/env python3

# Src: https://docs.python.org/3/library/sqlite3.html

import sqlite3

con = sqlite3.connect(":memory:")

cur = con.cursor()
cur.execute("create table lang (name, first_appeared)")

# This is the qmark style:
cur.execute("insert into lang values (?, ?)", ("C", 1972))

# The qmark style used with executemany():
lang_list = [
    ("Fortran", 1957),
    ("Python", 1991),
    ("Go", 2009),
]
cur.executemany("insert into lang values (?, ?)", lang_list)

# To retrieve data after executing a SELECT statement,
# you can either treat the cursor as an iterator,
# call the cursor’s fetchone() method to retrieve a single matching row,
# or call fetchall() to get a list of the matching rows.

for row in cur.execute('SELECT * FROM lang ORDER BY first_appeared'):
    print(row)

con.close()
