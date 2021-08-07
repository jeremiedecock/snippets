#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: http://doc.qt.io/qt-5/modelview.html#2-1-a-read-only-table

import sys
from PySide6 import QtCore, QtWidgets

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel


# INIT THE DATABASE #############################

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("./employee.db")
assert db.open()

# INSERT VALUES

q = QSqlQuery()
assert q.prepare("INSERT INTO employee(first_name, last_name) VALUES(?, ?)")

q.addBindValue("Jean")
q.addBindValue("Dupont")
q.exec()

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
