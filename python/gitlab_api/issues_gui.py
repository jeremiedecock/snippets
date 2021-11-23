#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: https://doc.qt.io/qtforpython/PySide6/QtSql/QSqlTableModel.html?highlight=qsqltablemodel

# TODO:
# - Ajouter un filtre "me" et un filtre "Meta" (sur les labels) + un filtre sur les numéros de sujets
# - Couleur du background défini par le label, comme sur les slides : en cours = orange, fini = vert, etc.

# TODO: REMPLACER PARTOUT LES NUMÉROS DE COLONNE ÉCRITS EN DURE PAR e.g. model.fieldIndex("description")
#        id               INTEGER,
#        state            TEXT,
#        title            TEXT,
#        description      TEXT,
#        labels           TEXT,
#        created_at       TEXT,
#        updated_at       TEXT,
#        milestone_id     INTEGER,
#        web_url          TEXT,
#        project_id       INTEGER,
#        iid              INTEGER,
#        upload_required  INTEGER,


import sys
import sqlite3
import webbrowser
import requests
import json
import urllib

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QSortFilterProxyModel, QModelIndex
from PySide6.QtWidgets import QApplication, QWidget, QSplitter, QDataWidgetMapper, QPlainTextEdit, QFormLayout, QTableView, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QAbstractItemView, QComboBox, QCheckBox
from PySide6.QtGui import QAction
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

MILESTONES_DICT = {
    "C3 Sprint 1": 204,
    "C3 Sprint 2": 205,
    "C3 Sprint 3": 206,
    "C3 Sprint 4": 207
}

with open("GITLAB_SECRET_TOKEN", "r") as fd:
    GITLAB_TOKEN = fd.read().strip()

with open("GITLAB_HOST", "r") as fd:
    GITLAB_HOST = fd.read().strip()

HEADER_DICT = {"PRIVATE-TOKEN": GITLAB_TOKEN}

# OPEN THE DATABASE #############################

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("./issues.sqlite")
assert db.open()


def put_request(put_url):
    resp = requests.put(put_url, headers=HEADER_DICT)

    if resp.status_code != 200:
        raise Exception("Error:" + resp.text)

    json_dict = json.loads(resp.text)
    return json_dict


def push_button_callback():
    selection_index_list = table_view.selectionModel().selectedRows()
    selected_row_list = [source_index.row() for source_index in selection_index_list]

    for row_index in sorted(selected_row_list, reverse=True):
        # Remove rows one by one to allow the removql of non-contiguously selected rows (e.g. "rows 0, 2 and 3")
        print(row_index, model.fieldIndex("description"))

        iid_index = model.index(row_index, model.fieldIndex("iid"))          # GET INDEX
        issue_iid = iid_index.data(Qt.EditRole)  

        project_id_index = model.index(row_index, model.fieldIndex("project_id"))          # GET INDEX
        project_id = project_id_index.data(Qt.EditRole)  

        description_index = model.index(row_index, model.fieldIndex("description"))          # GET INDEX
        description_str = description_index.data(Qt.EditRole)                                # GET DATA
        description_str = urllib.parse.quote(description_str)

        title_index = model.index(row_index, model.fieldIndex("title"))          # GET INDEX
        title_str = title_index.data(Qt.EditRole)                                # GET DATA
        title_str = urllib.parse.quote(title_str)

        labels_index = model.index(row_index, model.fieldIndex("labels"))          # GET INDEX
        labels_str = labels_index.data(Qt.EditRole)                                # GET DATA
        labels_str = urllib.parse.quote(labels_str)

        put_url = GITLAB_HOST + "/api/v4/projects/{}/issues/{}?title={}&labels={}&description={}".format(project_id, issue_iid, title_str, labels_str, description_str)
        #print(put_url)

        json_dict = put_request(put_url)
        print(json_dict)

    #model.submitAll()  # When you’re finished changing a record, you should always call submitAll() to ensure that the changes are written to the database
    #model.select()

#################################################

app = QApplication(sys.argv)
window = QWidget()

# Make widgets ##############

title_desc_filter_edit = QLineEdit()
title_desc_filter_edit.setPlaceholderText("Filter text (on title and description)")

milestone_combobox = QComboBox()
milestone_combobox.addItems(["*", "Meta"] + list(MILESTONES_DICT.keys()))
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

splitter = QSplitter(orientation=Qt.Vertical, parent=window)

table_view = QTableView(parent=splitter)

push_button = QPushButton('Push', parent=window)
push_button.clicked.connect(push_button_callback)

# Splitter

splitter.addWidget(table_view)

# Mapped widgets

description_widget = QPlainTextEdit(splitter)
splitter.addWidget(description_widget)
##set_mapped_widgets_enabled(False)
#description_widget.setPlainText("")
#description_widget.setPlaceholderText("")
#description_widget.setDisabled(True)

# Set the layout ############

vbox = QVBoxLayout()

filter_layout = QFormLayout()

# Filter form

filter_layout.addRow("Contains:", title_desc_filter_edit)
filter_layout.addRow("State:", state_combobox)
filter_layout.addRow("Milestone:", milestone_combobox)

vbox.addLayout(filter_layout)
vbox.addLayout(ft_hbox)
vbox.addWidget(splitter)
vbox.addWidget(push_button)

window.setLayout(vbox)

#############################

model = QSqlTableModel()
model.setTable("issues")
#model.setEditStrategy(QSqlTableModel.OnManualSubmit)
model.select()
model.setHeaderData(model.fieldIndex("id"), Qt.Horizontal, "ID")
model.setHeaderData(model.fieldIndex("state"), Qt.Horizontal, "State")
model.setHeaderData(model.fieldIndex("title"), Qt.Horizontal, "Title")
#model.setHeaderData(model.fieldIndex("description"), Qt.Horizontal, "Description")
model.setHeaderData(model.fieldIndex("labels"), Qt.Horizontal, "Labels")
model.setHeaderData(model.fieldIndex("created_at"), Qt.Horizontal, "Created at")
model.setHeaderData(model.fieldIndex("updated_at"), Qt.Horizontal, "Updated at")
#model.setHeaderData(model.fieldIndex("milestone_id"), Qt.Horizontal, "Milestone id")
#model.setHeaderData(model.fieldIndex("web_url"), Qt.Horizontal, "Web URL")
#model.setHeaderData(model.fieldIndex("project_id"), Qt.Horizontal, "Project ID")
model.setHeaderData(model.fieldIndex("iid"), Qt.Horizontal, "IID")
model.setHeaderData(model.fieldIndex("upload_required"), Qt.Horizontal, "Up")

table_view.setModel(model)
table_view.setSortingEnabled(True)
table_view.setSelectionBehavior(QAbstractItemView.SelectRows)    # Select the full row when a cell is selected (See http://doc.qt.io/qt-5/qabstractitemview.html#selectionBehavior-prop )
table_view.setAlternatingRowColors(True)

table_view.verticalHeader().setVisible(False)              # Hide the vertical header
table_view.horizontalHeader().setStretchLastSection(True)  # http://doc.qt.io/qt-5/qheaderview.html#stretchLastSection-prop

table_view.hideColumn(model.fieldIndex("description"))
table_view.hideColumn(model.fieldIndex("milestone_id"))
table_view.hideColumn(model.fieldIndex("web_url"))
table_view.hideColumn(model.fieldIndex("project_id"))

table_view.setColumnWidth(model.fieldIndex("id"), 50)
table_view.setColumnWidth(model.fieldIndex("state"), 60)
table_view.setColumnWidth(model.fieldIndex("title"), 1090)
table_view.setColumnWidth(model.fieldIndex("labels"), 400)
table_view.setColumnWidth(model.fieldIndex("iid"), 35)
table_view.setColumnWidth(model.fieldIndex("upload_required"), 25)

# SET QDATAWIDGETMAPPER ###########################

mapper = QDataWidgetMapper()
mapper.setModel(model)          # WARNING: do not use `self.table_source_model` here otherwise the index mapping will be wrong!
mapper.addMapping(description_widget, model.fieldIndex("Description"))

# https://doc.qt.io/qtforpython/examples/example_sql__books.html
selection_model = table_view.selectionModel()
selection_model.currentRowChanged.connect(mapper.setCurrentModelIndex)

table_view.setCurrentIndex(model.index(0, 0))

        #self.mapper.toFirst()                      # TODO: is it a good idea ?

#table_view.selectionModel().selectionChanged.connect(self.update_selection)

        # TODO: http://doc.qt.io/qt-5/qdatawidgetmapper.html#setCurrentModelIndex
        #self.table_view.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex())

        # TODO: https://doc-snapshots.qt.io/qtforpython/PySide2/QtWidgets/QDataWidgetMapper.html#PySide2.QtWidgets.PySide2.QtWidgets.QDataWidgetMapper.setCurrentModelIndex
        #connect(myTableView.selectionModel(), SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"),
        #mapper, SLOT(setCurrentModelIndex(QModelIndex)))


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
        if milestone_filter_str == 'Meta':
            global_filter_list.append("labels LIKE '%Meta%'")
        else:
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
        web_url = model.index(row_index, model.fieldIndex("web_url")).data()     # TODO
        print(web_url)
        webbrowser.open(web_url)


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
    #model.setData(model.index(row, model.fieldIndex("id")), 1013)
    model.setData(model.index(row, model.fieldIndex("state")), "opened")
    model.setData(model.index(row, model.fieldIndex("title")), "n/a")
    model.setData(model.index(row, model.fieldIndex("labels")), "n/a")
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

#window.show()
window.showMaximized()

# The mainloop of the application. The event handling starts from this point.
exit_code = app.exec()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
