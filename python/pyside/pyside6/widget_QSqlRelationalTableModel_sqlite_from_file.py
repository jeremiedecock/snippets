#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: https://doc.qt.io/qtforpython/PySide6/QtSql/QSqlRelationalTableModel.html?highlight=qsqlrelationaltablemodel

import sys
import sqlite3
from PySide6 import QtCore, QtWidgets

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate


# INIT THE DATABASE #############################

con = sqlite3.connect("employee2.db")
cur = con.cursor()

try:
    cur.execute("DROP TABLE t_employee")
except:
    pass

try:
    cur.execute("DROP TABLE t_country")
except:
    pass

cur.execute("CREATE TABLE t_country (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
cur.execute("CREATE TABLE t_employee (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, country_id TEXT, FOREIGN KEY(country_id) REFERENCES t_country(id))")

params_list = [
    ("France",),
    ("Belgium",),
    ("Germany",),
    ("Spain",),
    ("Italy",),
]

cur.executemany("INSERT INTO t_country (name) VALUES(?)", params_list)

params_list = [
    ("Jean", "Dupont", 2),
    ("Paul", "Dupond", 2),
    ("Jeanne", "Durand", 1),
    ("Anne", "Dupuit", 1),
]

cur.executemany("INSERT INTO t_employee (first_name, last_name, country_id) VALUES(?, ?, ?)", params_list)
con.commit()

con.close()


# OPEN THE DATABASE #############################

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("./employee2.db")
assert db.open()


#################################################

app = QApplication(sys.argv)

table_view = QTableView()
table_view.setSortingEnabled(True)

model = QSqlRelationalTableModel()
model.setTable("t_employee")
model.setRelation(3, QSqlRelation("t_country", "id", "name"))  # column 3 in table t_employee is a foreign key that maps with field id of table t_country, and that the view should present the country's name field to the user
model.select()
model.setHeaderData(0, Qt.Horizontal, "ID")
model.setHeaderData(1, Qt.Horizontal, "First Name")
model.setHeaderData(2, Qt.Horizontal, "Last Name")
model.setHeaderData(3, Qt.Horizontal, "Counrty")

table_view.setModel(model)
table_view.setItemDelegate(QSqlRelationalDelegate(table_view))


#################################################

table_view.show()

# The mainloop of the application. The event handling starts from this point.
exit_code = app.exec()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
