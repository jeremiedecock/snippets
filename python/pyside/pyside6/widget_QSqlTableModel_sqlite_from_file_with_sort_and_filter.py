#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: https://doc.qt.io/qtforpython/PySide6/QtSql/QSqlTableModel.html?highlight=qsqltablemodel

import sys
import sqlite3
from PySide6 import QtCore, QtWidgets

from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtWidgets import QApplication, QWidget, QTableView, QLineEdit, QVBoxLayout
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel


# INIT THE DATABASE #############################

con = sqlite3.connect("employee.db")
cur = con.cursor()

cur.execute("DROP TABLE employee")
cur.execute("CREATE TABLE employee (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT)")

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
window = QWidget()

# Make widgets ##############

edit = QLineEdit()
table_view = QTableView()

edit.setPlaceholderText("Filter text (on col. 1)")

# Set the layout ############

vbox = QVBoxLayout()

vbox.addWidget(edit)
vbox.addWidget(table_view)

window.setLayout(vbox)

#############################

model = QSqlTableModel()
model.setTable("employee")
#model.setEditStrategy(QSqlTableModel.OnManualSubmit)
model.select()
model.setHeaderData(0, Qt.Horizontal, "First Name")
model.setHeaderData(1, Qt.Horizontal, "Last Name")

table_view.setModel(model)
table_view.setSortingEnabled(True)

table_view.hideColumn(0) # don't show the ID

# Set LineEdit slot #########################

def foo():
    filter_str = edit.text()
    if filter_str == '':
        model.setFilter("")
    else:
        model.setFilter("first_name LIKE '%{}%'".format(filter_str))
    print(filter_str)


edit.textChanged.connect(foo)

#############################

window.show()

# The mainloop of the application. The event handling starts from this point.
exit_code = app.exec()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
