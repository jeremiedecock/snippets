#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: http://doc.qt.io/qt-5/modelview.html#2-1-a-read-only-table

import sys
from PySide6 import QtCore, QtWidgets

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel

from secret import PSQL_DBNAME, PSQL_USERNAME, PSQL_PASSWORD

# INIT THE DATABASE #############################

# https://doc.qt.io/qt-5/qsqldatabase.html#details
db = QSqlDatabase.addDatabase("QPSQL")
db.setHostName("localhost");
db.setDatabaseName(PSQL_DBNAME);
db.setUserName(PSQL_USERNAME);
db.setPassword(PSQL_PASSWORD);
assert db.open()

# CREATE TABLE

q = QSqlQuery()
#assert q.exec("CREATE TABLE employee(id INTEGER PRIMARY KEY, first_name VARCHAR, last_name VARCHAR)")

# INSERT VALUES

assert q.prepare("INSERT INTO employee(id, first_name, last_name) VALUES(?, ?, ?)")

q.addBindValue(3)
q.addBindValue("Jean")
q.addBindValue("Dupont")
q.exec()

q.addBindValue(4)
q.addBindValue("Paul")
q.addBindValue("Dupond")
q.exec()


#################################################

app = QApplication(sys.argv)

table_view = QTableView()

model = QSqlQueryModel()
model.setQuery("SELECT * FROM employee")

table_view.setModel(model)
table_view.show()

# The mainloop of the application. The event handling starts from this point.
exit_code = app.exec()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
