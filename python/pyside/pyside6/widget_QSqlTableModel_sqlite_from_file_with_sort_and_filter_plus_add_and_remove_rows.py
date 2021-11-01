#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: https://doc.qt.io/qtforpython/PySide6/QtSql/QSqlTableModel.html?highlight=qsqltablemodel

import sys
import sqlite3
from PySide6 import QtCore, QtWidgets

from PySide6.QtCore import Qt, QSortFilterProxyModel, QModelIndex
from PySide6.QtWidgets import QApplication, QWidget, QTableView, QLineEdit, QVBoxLayout, QAbstractItemView
from PySide6.QtGui import QAction
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
table_view.setSelectionBehavior(QAbstractItemView.SelectRows)    # Select the full row when a cell is selected (See http://doc.qt.io/qt-5/qabstractitemview.html#selectionBehavior-prop )

table_view.hideColumn(0) # don't show the ID

# Set LineEdit slot #########################

def filter_callback():
    filter_str = edit.text()
    if filter_str == '':
        model.setFilter("")
    else:
        model.setFilter("first_name LIKE '%{}%'".format(filter_str))
    print(filter_str)


edit.textChanged.connect(filter_callback)

#############################

def add_row_callback():
    # See https://doc.qt.io/qtforpython/overviews/sql-model.html#using-the-sql-model-classes
    row = 0
    model.insertRows(row, 1)
    #model.setData(model.index(row, 0), 1013)
    model.setData(model.index(row, 1), "n/a")
    model.setData(model.index(row, 2), "n/a")
    model.submitAll()
    #model.select()

def remove_row_callback():
    # See https://doc.qt.io/qt-5/qsqltablemodel.html#removeRows
    # See https://doc.qt.io/qtforpython/overviews/sql-model.html#using-the-sql-model-classes
    # See http://doc.qt.io/qt-5/model-view-programming.html#handling-selections-in-item-views

    selection_proxy_index_list = table_view.selectionModel().selectedRows()
    selected_row_list = [source_index.row() for source_index in selection_proxy_index_list]

    for row_index in sorted(selected_row_list, reverse=True):
        # Remove rows one by one to allow the removql of non-contiguously selected rows (e.g. "rows 0, 2 and 3")
        success = model.removeRow(row_index)
        if not success:
            raise Exception("Unknown error...")   # TODO

    model.submitAll()  # When you’re finished changing a record, you should always call submitAll() to ensure that the changes are written to the database
    model.select()

# Add row action
add_action = QAction(table_view)
add_action.setShortcut(Qt.CTRL | Qt.Key_N)
add_action.triggered.connect(add_row_callback)
table_view.addAction(add_action)

# Delete action
del_action = QAction(table_view)
del_action.setShortcut(Qt.Key_Delete)
del_action.triggered.connect(remove_row_callback)
table_view.addAction(del_action)

#############################

window.show()

# The mainloop of the application. The event handling starts from this point.
exit_code = app.exec()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
