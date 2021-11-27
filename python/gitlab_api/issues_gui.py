#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: https://doc.qt.io/qtforpython/PySide6/QtSql/QSqlTableModel.html?highlight=qsqltablemodel

# TODO:
# - Ajouter un filtre "me" et un filtre "Meta" (sur les labels) + un filtre sur les numéros de sujets
# - Couleur du background défini par le label, comme sur les slides : en cours = orange, fini = vert, etc.

# TODO: REMPLACER PARTOUT LES NUMÉROS DE COLONNE ÉCRITS EN DURE PAR e.g. self.model.fieldIndex("description")
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
import logging

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QSortFilterProxyModel, QModelIndex
from PySide6.QtWidgets import QApplication, QWidget, QSplitter, QDataWidgetMapper, QPlainTextEdit, QFormLayout, QTableView, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QAbstractItemView, QComboBox, QCheckBox
from PySide6.QtGui import QAction
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

PROJECT_ID = 80
CURRENT_MILESTONE_ID = 207
DEFAULT_LABELS = "FT::IA,W::Backlog"

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

HEADER_DICT = {
    "PRIVATE-TOKEN": GITLAB_TOKEN,
    "Content-Type": "application/json"
}

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # OPEN THE DATABASE #############################

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("./issues.sqlite")
        assert db.open()

        # Make widgets ##############

        self.title_desc_filter_edit = QLineEdit()
        self.title_desc_filter_edit.setPlaceholderText("Filter text (on title and description)")

        self.milestone_combobox = QComboBox()
        self.milestone_combobox.addItems(["*", "Meta"] + list(MILESTONES_DICT.keys()))
        self.milestone_combobox.setCurrentText("*")

        self.state_combobox = QComboBox()
        self.state_combobox.addItems(["*", "opened", "closed"])
        self.state_combobox.setCurrentText("*")

        ft_hbox = QHBoxLayout()

        self.ft_ia_cb = QCheckBox('FT IA')
        self.ft_data_cb = QCheckBox('FT Data')
        self.ft_ops_cb = QCheckBox('FT Ops')
        self.ft_scale_cb = QCheckBox('FT Scale')
        self.ft_perf_cb = QCheckBox('FT Perf')

        ft_hbox.addWidget(self.ft_ia_cb)
        ft_hbox.addWidget(self.ft_data_cb)
        ft_hbox.addWidget(self.ft_ops_cb)
        ft_hbox.addWidget(self.ft_scale_cb)
        ft_hbox.addWidget(self.ft_perf_cb)

        state_hbox = QVBoxLayout()

        splitter = QSplitter(orientation=Qt.Vertical, parent=self)

        self.table_view = QTableView(parent=splitter)

        push_button = QPushButton('Push', parent=self)
        push_button.clicked.connect(self.push_button_callback)

        # Splitter

        splitter.addWidget(self.table_view)

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

        filter_layout.addRow("Contains:", self.title_desc_filter_edit)
        filter_layout.addRow("State:", self.state_combobox)
        filter_layout.addRow("Milestone:", self.milestone_combobox)

        vbox.addLayout(filter_layout)
        vbox.addLayout(ft_hbox)
        vbox.addWidget(splitter)
        vbox.addWidget(push_button)

        self.setLayout(vbox)

        #############################

        self.model = QSqlTableModel()
        self.model.setTable("issues")
        #self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()
        self.model.setHeaderData(self.model.fieldIndex("id"), Qt.Horizontal, "ID")
        self.model.setHeaderData(self.model.fieldIndex("state"), Qt.Horizontal, "State")
        self.model.setHeaderData(self.model.fieldIndex("title"), Qt.Horizontal, "Title")
        #self.model.setHeaderData(self.model.fieldIndex("description"), Qt.Horizontal, "Description")
        self.model.setHeaderData(self.model.fieldIndex("labels"), Qt.Horizontal, "Labels")
        self.model.setHeaderData(self.model.fieldIndex("created_at"), Qt.Horizontal, "Created at")
        self.model.setHeaderData(self.model.fieldIndex("updated_at"), Qt.Horizontal, "Updated at")
        #self.model.setHeaderData(self.model.fieldIndex("milestone_id"), Qt.Horizontal, "Milestone id")
        #self.model.setHeaderData(self.model.fieldIndex("web_url"), Qt.Horizontal, "Web URL")
        #self.model.setHeaderData(self.model.fieldIndex("project_id"), Qt.Horizontal, "Project ID")
        self.model.setHeaderData(self.model.fieldIndex("iid"), Qt.Horizontal, "IID")
        self.model.setHeaderData(self.model.fieldIndex("upload_required"), Qt.Horizontal, "Up")

        self.table_view.setModel(self.model)
        self.table_view.setSortingEnabled(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)    # Select the full row when a cell is selected (See http://doc.qt.io/qt-5/qabstractitemview.html#selectionBehavior-prop )
        self.table_view.setAlternatingRowColors(True)

        self.table_view.verticalHeader().setVisible(False)              # Hide the vertical header
        self.table_view.horizontalHeader().setStretchLastSection(True)  # http://doc.qt.io/qt-5/qheaderview.html#stretchLastSection-prop

        self.table_view.hideColumn(self.model.fieldIndex("description"))
        self.table_view.hideColumn(self.model.fieldIndex("milestone_id"))
        self.table_view.hideColumn(self.model.fieldIndex("web_url"))
        self.table_view.hideColumn(self.model.fieldIndex("project_id"))

        self.table_view.setColumnWidth(self.model.fieldIndex("id"), 50)
        self.table_view.setColumnWidth(self.model.fieldIndex("state"), 60)
        self.table_view.setColumnWidth(self.model.fieldIndex("title"), 1090)
        self.table_view.setColumnWidth(self.model.fieldIndex("labels"), 400)
        self.table_view.setColumnWidth(self.model.fieldIndex("iid"), 35)
        self.table_view.setColumnWidth(self.model.fieldIndex("upload_required"), 25)

        # SET QDATAWIDGETMAPPER ###########################

        mapper = QDataWidgetMapper()
        mapper.setModel(self.model)          # WARNING: do not use `self.table_source_self.model` here otherwise the index mapping will be wrong!
        mapper.addMapping(description_widget, self.model.fieldIndex("Description"))

        # https://doc.qt.io/qtforpython/examples/example_sql__books.html
        selection_model = self.table_view.selectionModel()
        selection_model.currentRowChanged.connect(mapper.setCurrentModelIndex)


        self.table_view.setCurrentIndex(self.model.index(0, 0))

                #self.mapper.toFirst()                      # TODO: is it a good idea ?

        #self.table_view.selectionModel().selectionChanged.connect(self.update_selection)

                # TODO: http://doc.qt.io/qt-5/qdatawidgetmapper.html#setCurrentModelIndex
                #self.self.table_view.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex())

                # TODO: https://doc-snapshots.qt.io/qtforpython/PySide2/QtWidgets/QDataWidgetMapper.html#PySide2.QtWidgets.PySide2.QtWidgets.QDataWidgetMapper.setCurrentModelIndex
                #connect(myTableView.selectionModel(), SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"),
                #mapper, SLOT(setCurrentModelIndex(QModelIndex)))

        self.title_desc_filter_edit.textChanged.connect(self.filter_callback)
        self.milestone_combobox.currentIndexChanged.connect(self.filter_callback)
        self.state_combobox.currentIndexChanged.connect(self.filter_callback)
        self.ft_ia_cb.stateChanged.connect(self.filter_callback)
        self.ft_data_cb.stateChanged.connect(self.filter_callback)
        self.ft_ops_cb.stateChanged.connect(self.filter_callback)
        self.ft_scale_cb.stateChanged.connect(self.filter_callback)
        self.ft_perf_cb.stateChanged.connect(self.filter_callback)

        # Open web page action

        open_action = QAction(self.table_view)
        open_action.setShortcut(Qt.CTRL | Qt.Key_Space)

        open_action.triggered.connect(self.open_action_callback)
        self.table_view.addAction(open_action)

        # Push action

        push_action = QAction(self.table_view)
        push_action.setShortcut(Qt.CTRL | Qt.Key_S)

        push_action.triggered.connect(self.push_button_callback)
        self.table_view.addAction(push_action)

        # Add row action
        add_action = QAction(self.table_view)
        add_action.setShortcut(Qt.CTRL | Qt.Key_N)
        add_action.triggered.connect(self.add_row_callback)
        self.table_view.addAction(add_action)

        # Delete action
        del_action = QAction(self.table_view)
        del_action.setShortcut(Qt.Key_Delete)
        del_action.triggered.connect(self.remove_row_callback)
        self.table_view.addAction(del_action)


    #def put_request(put_url):
    #    resp = requests.put(put_url, headers=HEADER_DICT)
    #
    #    if resp.status_code != 200:
    #        raise Exception("Error:" + resp.text)
    #
    #    json_dict = json.loads(resp.text)
    #    return json_dict


    def put_request(self, put_url, data_dict):
        # https://docs.gitlab.com/ee/api/#request-payload
        resp = requests.put(put_url, json=data_dict, headers=HEADER_DICT)

        if resp.status_code != 200:
            raise Exception("Error:" + resp.text)

        json_dict = json.loads(resp.text)
        return json_dict


    def push_button_callback(self):
        selection_index_list = self.table_view.selectionModel().selectedRows()
        selected_row_list = [source_index.row() for source_index in selection_index_list]

        for row_index in sorted(selected_row_list, reverse=True):
            # Remove rows one by one to allow the removql of non-contiguously selected rows (e.g. "rows 0, 2 and 3")
            print(row_index, self.model.fieldIndex("description"))

            iid_index = self.model.index(row_index, self.model.fieldIndex("iid"))          # GET INDEX
            issue_iid = iid_index.data(Qt.EditRole)  

            project_id_index = self.model.index(row_index, self.model.fieldIndex("project_id"))          # GET INDEX
            project_id = project_id_index.data(Qt.EditRole)  

            description_index = self.model.index(row_index, self.model.fieldIndex("description"))          # GET INDEX
            description_str = description_index.data(Qt.EditRole)                                # GET DATA
            #description_str = urllib.parse.quote(description_str)

            title_index = self.model.index(row_index, self.model.fieldIndex("title"))          # GET INDEX
            title_str = title_index.data(Qt.EditRole)                                # GET DATA
            #title_str = urllib.parse.quote(title_str)

            labels_index = self.model.index(row_index, self.model.fieldIndex("labels"))          # GET INDEX
            labels_str = labels_index.data(Qt.EditRole)                                # GET DATA
            #labels_str = urllib.parse.quote(labels_str)

            #put_url = GITLAB_HOST + "/api/v4/projects/{}/issues/{}?title={}&labels={}&description={}".format(project_id, issue_iid, title_str, labels_str, description_str)
            put_url = GITLAB_HOST + "/api/v4/projects/{}/issues/{}".format(project_id, issue_iid)
            #print(put_url)

            data_dict = {
                "title": title_str,
                "description": description_str
            }

            json_dict = self.put_request(put_url, data_dict)
            print(json_dict)

        #self.model.submitAll()  # When you’re finished changing a record, you should always call submitAll() to ensure that the changes are written to the database
        #self.model.select()



    # Set LineEdit slot #########################

    def filter_callback(self):
        title_desc_filter_str = self.title_desc_filter_edit.text()
        milestone_filter_str = self.milestone_combobox.currentText()
        state_filter_str = self.state_combobox.currentText()

        global_filter_list = []
        ft_filter_list = []

        if title_desc_filter_str != '':
            global_filter_list.append("(title LIKE '{}' OR description LIKE '{}')".format('%' + title_desc_filter_str + '%', '%' + title_desc_filter_str + '%'))
        if milestone_filter_str != '*':
            if milestone_filter_str == 'Meta':
                global_filter_list.append(r"labels LIKE '%Meta%'")
            else:
                global_filter_list.append("milestone_id = {}".format(MILESTONES_DICT[milestone_filter_str]))
        if state_filter_str != '*':
            global_filter_list.append("state = '{}'".format(state_filter_str))
        if self.ft_ia_cb.isChecked():
            ft_filter_list.append(r"labels LIKE '%FT::IA%'")
        if self.ft_data_cb.isChecked():
            ft_filter_list.append(r"labels LIKE '%FT::Data%'")
        if self.ft_ops_cb.isChecked():
            ft_filter_list.append(r"labels LIKE '%FT::Ops%'")
        if self.ft_scale_cb.isChecked():
            ft_filter_list.append(r"labels LIKE '%FT::Scale%'")
        if self.ft_perf_cb.isChecked():
            ft_filter_list.append(r"labels LIKE '%FT::Perf%'")

        if len(ft_filter_list) > 0:
            ft_filter_str = " OR ".join(ft_filter_list)
            global_filter_list.append("(" + ft_filter_str + ")" )

        global_filter_str = "" if len(global_filter_list) == 0 else " AND ".join(global_filter_list)
        self.model.setFilter(global_filter_str)

        print(global_filter_str)


    def open_action_callback(self):
        # See https://doc.qt.io/qt-5/qsqltablemodel.html#removeRows
        # See https://doc.qt.io/qtforpython/overviews/sql-model.html#using-the-sql-model-classes
        # See http://doc.qt.io/qt-5/model-view-programming.html#handling-selections-in-item-views

        selection_index_list = self.table_view.selectionModel().selectedRows()
        selected_row_list = [source_index.row() for source_index in selection_index_list]

        for row_index in sorted(selected_row_list):
            web_url = self.model.index(row_index, self.model.fieldIndex("web_url")).data()     # TODO
            print(web_url)
            webbrowser.open(web_url)


    #############################

    def add_row_callback(self):
        # See https://doc.qt.io/qtforpython/overviews/sql-model.html#using-the-sql-model-classes

        #db = self.model.database()   # OK ! (but useless here...)
        #query = self.model.query()   # OK ???
        query = QSqlQuery()
        query.exec("SELECT MIN(id) FROM issues")
        query.next()
        min_id = query.value(0)

        new_id = min_id - 1 if min_id < 0 else -1
        print(min_id, new_id)

        #row_index = 0
        #self.model.insertRows(row_index, 1)
        #self.model.setData(self.model.index(row_index, self.model.fieldIndex("id")), new_id)
        #self.model.setData(self.model.index(row_index, self.model.fieldIndex("state")), "opened")
        #self.model.setData(self.model.index(row_index, self.model.fieldIndex("labels")), DEFAULT_LABELS)
        #self.model.setData(self.model.index(row_index, self.model.fieldIndex("milestone_id")), CURRENT_MILESTONE_ID)
        #self.model.setData(self.model.index(row_index, self.model.fieldIndex("project_id")), PROJECT_ID)
        #self.model.setData(self.model.index(row_index, self.model.fieldIndex("upload_required")), 1)
        #self.model.submitAll()
        #self.model.select()

        new_record = self.model.record()
        new_record.setValue("id", new_id)
        new_record.setValue("state", "opened")
        new_record.setValue("labels", DEFAULT_LABELS)
        new_record.setValue("milestone_id", CURRENT_MILESTONE_ID)
        new_record.setValue("project_id", PROJECT_ID)
        new_record.setValue("upload_required", 1)

        if not self.model.insertRecord(-1, new_record):
            logging.error("Failed to create new issue: {self.model.lastError().text()}")
            return

        self.model.submitAll()
        self.model.select()


    def remove_row_callback(self):
        """
        This callback remove selected rows from the LOCAL DATABASE ONLY!
        Locally removed rows won't be removed from the remote GitLab database
        (on purpose for safety reasons to avoid disastrous accidental actions).
        """
        # See https://doc.qt.io/qt-5/qsqltablemodel.html#removeRows
        # See https://doc.qt.io/qtforpython/overviews/sql-model.html#using-the-sql-model-classes
        # See http://doc.qt.io/qt-5/model-view-programming.html#handling-selections-in-item-views

        selection_index_list = self.table_view.selectionModel().selectedRows()
        selected_row_list = [source_index.row() for source_index in selection_index_list]

        for row_index in sorted(selected_row_list, reverse=True):
            # Remove rows one by one to allow the removql of non-contiguously selected rows (e.g. "rows 0, 2 and 3")
            success = self.model.removeRow(row_index)
            if not success:
                raise Exception("Unknown error...")   # TODO

        self.model.submitAll()  # When you’re finished changing a record, you should always call submitAll() to ensure that the changes are written to the database
        self.model.select()


#############################

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    window.showMaximized()

    # The mainloop of the application. The event handling starts from this point.
    exit_code = app.exec()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)