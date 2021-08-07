#!/bin/sh

# https://stackoverflow.com/questions/11643611/execute-sqlite-script

sqlite3 employee.db '.read init_sqlite_db.sql'
sqlite3 employee.db 'SELECT * FROM employee;'
