#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: https://doc.qt.io/qtforpython/PySide6/QtSql/QSqlTableModel.html?highlight=qsqltablemodel

import sys
import sqlite3
from PySide6 import QtCore, QtWidgets

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel


# INIT THE DATABASE #############################

con = sqlite3.connect("employee.db")
cur = con.cursor()

cur.execute("DROP TABLE employee")
cur.execute("CREATE TABLE employee (first_name TEXT, last_name TEXT)")

params_list = [
    ("Jean", "Dupont"),
    ("Paul", "Dupond"),
    ("Jeanne", "Durand"),
    ("Anne", "Dupuit"),
]

cur.executemany("INSERT INTO employee (first_name, last_name) VALUES(?, ?)", params_list)
con.commit()

con.close()

# OPEN THE DATABASE #############################

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("./employee.db")
assert db.open()

#################################################

app = QApplication(sys.argv)

table_view = QTableView()

model = QSqlTableModel()
model.setTable("employee")
model.select()

table_view.setModel(model)
table_view.show()

# The mainloop of the application. The event handling starts from this point.
exit_code = app.exec()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
