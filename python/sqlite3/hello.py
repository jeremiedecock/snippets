#!/usr/bin/env python3

# Src: https://docs.python.org/3/library/sqlite3.html

import sqlite3

con = sqlite3.connect('hello.db')

cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE book
               (title text, author text, pub_date text, price real)''')

# Insert a row of data
cur.execute("INSERT INTO book VALUES ('Reinforcement Learning an Introduction','Richard S. Sutton and Andrew G. Barto','2018-11-13',67.80)")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
