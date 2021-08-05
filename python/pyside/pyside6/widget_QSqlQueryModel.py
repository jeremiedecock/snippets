#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: http://doc.qt.io/qt-5/modelview.html#2-1-a-read-only-table

import sys
from PySide6 import QtCore, QtWidgets

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel


def add_employee(q, first_name, last_name):
    q.addBindValue(first_name)
    q.addBindValue(last_name)
    q.exec()

EMPLOYEE_SQL = """
    create table employee(id integer primary key, first_name varchar, last_name varchar)
    """

INSERT_EMPLOYEE_SQL = """
    insert into employee(first_name, last_name)
                values(?, ?)
    """

def init_db():
    def check(func, *args):
        if not func(*args):
            raise ValueError(func.__self__.lastError())

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(":memory:")

    check(db.open)

    q = QSqlQuery()
    check(q.exec, EMPLOYEE_SQL)

    check(q.prepare, INSERT_EMPLOYEE_SQL)
    add_employee(q, "Dupont", "Paul")
    add_employee(q, "Dupond", "Jean")

#################################################

app = QApplication(sys.argv)

init_db()

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
