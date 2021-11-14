#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: https://doc.qt.io/qtforpython/PySide6/QtSql/QSqlTableModel.html?highlight=qsqltablemodel

# TODO:
# - Ajouter un filtre "me" et un filtre "Meta" (sur les labels) + un filtre sur les numéros de sujets
# - Couleur du background défini par le label, comme sur les slides : en cours = orange, fini = vert, etc.

import sys
import sqlite3
from PySide6 import QtCore, QtWidgets

from PySide6.QtCore import Qt, QSortFilterProxyModel, QModelIndex
from PySide6.QtWidgets import QApplication, QWidget, QTableView, QLineEdit, QHBoxLayout, QVBoxLayout, QAbstractItemView, QComboBox, QCheckBox
from PySide6.QtGui import QAction
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

MILESTONES_DICT = {
    "C3 Sprint 1": 204,
    "C3 Sprint 2": 205,
    "C3 Sprint 3": 206,
    "C3 Sprint 4": 207
}

# OPEN THE DATABASE #############################

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("./issues.sqlite")
assert db.open()

#################################################

app = QApplication(sys.argv)
window = QWidget()

# Make widgets ##############

title_desc_filter_edit = QLineEdit()

milestone_combobox = QComboBox()
milestone_combobox.addItems(["*"] + list(MILESTONES_DICT.keys()))
milestone_combobox.setCurrentText("*")

state_combobox = QComboBox()
state_combobox.addItems(["*", "opened", "closed"])
state_combobox.setCurrentText("*")

ft_hbox = QHBoxLayout()

ft_ia_cb = QCheckBox('FT IA')
ft_data_cb = QCheckBox('FT Data')
ft_ops_cb = QCheckBox('FT Ops')
ft_scale_cb = QCheckBox('FT Scale')
ft_perf_cb = QCheckBox('FT Perf')

ft_hbox.addWidget(ft_ia_cb)
ft_hbox.addWidget(ft_data_cb)
ft_hbox.addWidget(ft_ops_cb)
ft_hbox.addWidget(ft_scale_cb)
ft_hbox.addWidget(ft_perf_cb)

state_hbox = QVBoxLayout()

table_view = QTableView()

title_desc_filter_edit.setPlaceholderText("Filter text (on title and description)")

# Set the layout ############

vbox = QVBoxLayout()

vbox.addWidget(title_desc_filter_edit)
vbox.addWidget(milestone_combobox)
vbox.addWidget(state_combobox)
vbox.addLayout(ft_hbox)
vbox.addWidget(table_view)

window.setLayout(vbox)

#############################

model = QSqlTableModel()
model.setTable("issues")
#model.setEditStrategy(QSqlTableModel.OnManualSubmit)
model.select()
model.setHeaderData(0, Qt.Horizontal, "ID")
model.setHeaderData(1, Qt.Horizontal, "State")
model.setHeaderData(2, Qt.Horizontal, "Title")
model.setHeaderData(3, Qt.Horizontal, "Description")
model.setHeaderData(4, Qt.Horizontal, "Labels")
model.setHeaderData(5, Qt.Horizontal, "Updated at")
model.setHeaderData(6, Qt.Horizontal, "Milestone id")
model.setHeaderData(7, Qt.Horizontal, "Web URL")
model.setHeaderData(8, Qt.Horizontal, "Upload required")

table_view.setModel(model)
table_view.setSortingEnabled(True)
table_view.setSelectionBehavior(QAbstractItemView.SelectRows)    # Select the full row when a cell is selected (See http://doc.qt.io/qt-5/qabstractitemview.html#selectionBehavior-prop )

#table_view.hideColumn(0) # don't show the ID
table_view.hideColumn(3) # don't show the ID
table_view.hideColumn(6) # don't show the ID
table_view.hideColumn(7) # don't show the ID
table_view.hideColumn(8) # don't show the ID


# Set LineEdit slot #########################

def filter_callback():
    title_desc_filter_str = title_desc_filter_edit.text()
    milestone_filter_str = milestone_combobox.currentText()
    state_filter_str = state_combobox.currentText()

    global_filter_list = []
    ft_filter_list = []

    if title_desc_filter_str != '':
        global_filter_list.append("(title LIKE '{}' OR description LIKE '{}')".format('%' + title_desc_filter_str + '%', '%' + title_desc_filter_str + '%'))
    if milestone_filter_str != '*':
        global_filter_list.append("milestone_id = {}".format(MILESTONES_DICT[milestone_filter_str]))
    if state_filter_str != '*':
        global_filter_list.append("state = '{}'".format(state_filter_str))
    if ft_ia_cb.isChecked():
        ft_filter_list.append("labels LIKE '%FT::IA%'")
    if ft_data_cb.isChecked():
        ft_filter_list.append("labels LIKE '%FT::Data%'")
    if ft_ops_cb.isChecked():
        ft_filter_list.append("labels LIKE '%FT::Ops%'")
    if ft_scale_cb.isChecked():
        ft_filter_list.append("labels LIKE '%FT::Scale%'")
    if ft_perf_cb.isChecked():
        ft_filter_list.append("labels LIKE '%FT::Perf%'")

    if len(ft_filter_list) > 0:
        ft_filter_str = " OR ".join(ft_filter_list)
        global_filter_list.append("(" + ft_filter_str + ")" )

    global_filter_str = "" if len(global_filter_list) == 0 else " AND ".join(global_filter_list)
    model.setFilter(global_filter_str)

    print(global_filter_str)


def open_action_callback():
    # See https://doc.qt.io/qt-5/qsqltablemodel.html#removeRows
    # See https://doc.qt.io/qtforpython/overviews/sql-model.html#using-the-sql-model-classes
    # See http://doc.qt.io/qt-5/model-view-programming.html#handling-selections-in-item-views

    selection_index_list = table_view.selectionModel().selectedRows()
    selected_row_list = [source_index.row() for source_index in selection_index_list]

    for row_index in sorted(selected_row_list):
        web_url = model.index(row_index, 7).data()     # TODO
        print(web_url)


title_desc_filter_edit.textChanged.connect(filter_callback)
milestone_combobox.currentIndexChanged.connect(filter_callback)
state_combobox.currentIndexChanged.connect(filter_callback)
ft_ia_cb.stateChanged.connect(filter_callback)
ft_data_cb.stateChanged.connect(filter_callback)
ft_ops_cb.stateChanged.connect(filter_callback)
ft_scale_cb.stateChanged.connect(filter_callback)
ft_perf_cb.stateChanged.connect(filter_callback)

# Open web page action

open_action = QAction(table_view)
open_action.setShortcut(Qt.CTRL | Qt.Key_Space)

open_action.triggered.connect(open_action_callback)
table_view.addAction(open_action)

#############################

def add_row_callback():
    # See https://doc.qt.io/qtforpython/overviews/sql-model.html#using-the-sql-model-classes
    row = 0
    model.insertRows(row, 1)
    #model.setData(model.index(row, 0), 1013)
    model.setData(model.index(row, 1), "n/a")
    model.setData(model.index(row, 2), "n/a")
    model.setData(model.index(row, 3), "n/a")
    model.submitAll()
    #model.select()

def remove_row_callback():
    # See https://doc.qt.io/qt-5/qsqltablemodel.html#removeRows
    # See https://doc.qt.io/qtforpython/overviews/sql-model.html#using-the-sql-model-classes
    # See http://doc.qt.io/qt-5/model-view-programming.html#handling-selections-in-item-views

    selection_index_list = table_view.selectionModel().selectedRows()
    selected_row_list = [source_index.row() for source_index in selection_index_list]

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
