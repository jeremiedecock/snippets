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
import datetime
import logging
import traceback

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QSortFilterProxyModel, QModelIndex, QRunnable, Slot, Signal, QObject, QThreadPool
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QSizePolicy, QLabel, QMessageBox, QSplitter, QDataWidgetMapper, QPlainTextEdit, QFormLayout, QTableView, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QAbstractItemView, QComboBox, QCheckBox
from PySide6.QtGui import QAction
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelationalTableModel

PUSH_NUM_ROWS_ALERT_THRESHOLD = 1
DEFAULT_PROJECT_ID = 80
DEFAULT_LABELS = "FT::IA,W::Backlog"

SQLITE_FILE_PATH = "issues.sqlite"
ISSUES_TABLE_NAME = "issues"
MILESTONES_TABLE_NAME = "milestones"

MILESTONES_DICT = {
    "C3 Sprint 1": 204,
    "C3 Sprint 2": 205,
    "C3 Sprint 3 (Nov  1, 2021 - Nov 12, 2021)": 206,
    "C3 Sprint 4 (Nov 15, 2021 - Nov 26, 2021)": 207,
    "C3 Sprint 5 (Nov 29, 2021 - Dec 10, 2021)": 209
}

MILESTONES_DICT2 = {     # Workaround
    "C3 Sprint 1": "C3 Sprint 1",
    "C3 Sprint 2": "C3 Sprint 2",
    "C3 Sprint 3 (Nov  1, 2021 - Nov 12, 2021)": "C3 Sprint 3",
    "C3 Sprint 4 (Nov 15, 2021 - Nov 26, 2021)": "C3 Sprint 4 - Current",
    "C3 Sprint 5 (Nov 29, 2021 - Dec 10, 2021)": "C3 Sprint 5 - Next"
}

CURRENT_MILESTONE_ID = 209


with open("GITLAB_SECRET_TOKEN", "r") as fd:
    GITLAB_TOKEN = fd.read().strip()

with open("GITLAB_HOST", "r") as fd:
    GITLAB_HOST = fd.read().strip()

HEADER_DICT = {
    "PRIVATE-TOKEN": GITLAB_TOKEN,
    "Content-Type": "application/json",
    "charset": "utf-8"
}

def str_to_datetime(datetime_str):
    """e.g. : 2021-11-16T16:07:05.688Z (GITLAB FORMAT) -> 2021-11-16T16:07:05.688+00:00 (SQLITE FORMAT)"""
    return datetime.datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))


def get_request(get_url):
    """
    https://docs.gitlab.com/ee/api/issues.html

    Parameters
    ----------
    get_url : [type]
        [description]

    Returns
    -------
    [type]
        [description]

    Raises
    ------
    Exception
        [description]
    Exception
        [description]
    Exception
        [description]
    """
    resp = requests.get(get_url, headers=HEADER_DICT)

    json_list = json.loads(resp.text)
    if resp.status_code != 200:
        raise Exception("Error:" + resp.text)
    if resp.encoding.lower() != 'utf-8':
        raise Exception("Encoding error:", resp.encoding)
    if resp.apparent_encoding.lower() != 'utf-8':
        raise Exception("Apparent_encoding error:", resp.apparent_encoding)

    for issue_dict in json_list:
        if ("Ã©" in issue_dict["title"]) or ("â€™" in issue_dict["title"]) or ("Ã‰" in issue_dict["title"]) or ("Ã¢" in issue_dict["title"]): # Ã¨
            print("Encoding err:", issue_dict["id"], issue_dict["web_url"])

    return json_list, resp


def fetch_issues(update_after=None, progress_callback=None):
    """
    [summary]

    Parameters
    ----------
    update_after : [type], optional
        [description], by default None

    Returns
    -------
    [type]
        [description]
    """
    issue_list = []

    params_str = "updated_after={},".format(update_after) if update_after is not None else ""

    json_list, resp = get_request(GITLAB_HOST + "/api/v4/issues?{}per_page=100&page=1&scope=all".format(params_str))
    num_pages = int(resp.headers['X-Total-Pages'])

    for page in range(2, num_pages+1):
        if progress_callback is not None:
            progress_callback.emit(int(page/num_pages * 100))
        msg = "page {}/{}".format(page, num_pages)
        print(msg)
        #main_window.statusBar().showMessage(msg, 2000)

        issue_list.extend(json_list)
        next_page = GITLAB_HOST + "/api/v4/issues?{}per_page=100&page={}&scope=all".format(params_str, page)
        json_list, resp = get_request(next_page)

    return issue_list


def fetch_selected_issues(project_iid_list, progress_callback=None):
    """
    [summary]

    Parameters
    ----------
    project_iid_list : list
        [description], by default None

    Returns
    -------
    [type]
        [description]
    """

    iid_dict = {}
    for project_id, iid in project_iid_list:
        if project_id not in iid_dict:
            iid_dict[project_id] = []
        iid_dict[project_id].append(iid)

    issue_list = []

    # Group requests per project id
    for project_id, iid_list in iid_dict.items():
        url = GITLAB_HOST + "/api/v4/projects/{}/issues?per_page=100&page={}&scope=all"

        for iid in iid_list:
            url += "&iids[]={}".format(iid)

        json_list, resp = get_request(url.format(project_id, 1))
        issue_list.extend(json_list)

        num_pages = int(resp.headers['X-Total-Pages'])

        for page in range(2, num_pages+1):
            if progress_callback is not None:
                progress_callback.emit(int(page/num_pages * 100))
            print("page {}/{}".format(page, num_pages))

            json_list, resp = get_request(url.format(project_id, page))
            issue_list.extend(json_list)

    return issue_list



def make_sqlite_database(issue_list):
    con = sqlite3.connect(SQLITE_FILE_PATH)
    cur = con.cursor()

#    # MILESTONES ################################
# 
#    # DELETE TABLE ##############
# 
#    try:
#        cur.execute("DROP TABLE {}".format(MILESTONES_TABLE_NAME))
#    except:
#        pass
# 
#    # CREATE TABLE ##############
# 
#    sql_query_str = """CREATE TABLE {} (
#        id               INTEGER,
#        title            TEXT,
#        PRIMARY KEY (id)
#    )""".format(MILESTONES_TABLE_NAME)
# 
#    cur.execute(sql_query_str)
# 
#    # INSERT SQL DATA ###########
#
#    # "milestone" : {
#    #     "project_id" : 1,
#    #     "description" : "Ducimus nam enim ex consequatur cumque ratione.",
#    #     "state" : "closed",
#    #     "due_date" : null,
#    #     "iid" : 2,
#    #     "created_at" : "2016-01-04T15:31:39.996Z",
#    #     "title" : "v4.0",
#    #     "id" : 17,
#    #     "updated_at" : "2016-01-04T15:31:39.996Z"
#    # },
#
#    milestones_dict = {}
#
#    for issue_dict in issue_list:
#        milestone_id = issue_dict["milestone"]["id"]
#        if milestone_id not in milestones_dict:
#            milestone_title = issue_dict["milestone"]["title"]
#            milestones_dict[milestone_id] = milestone_title
#
#    sql_insert_params = [(key, value) for key, value in milestones_dict.items()]
#
#    #(204, "C3 Sprint 1"),
#    #(205, "C3 Sprint 2"),
#    #(206, "C3 Sprint 3 (Nov  1, 2021 - Nov 12, 2021)"),
#    #(207, "C3 Sprint 4 (Nov 15, 2021 - Nov 26, 2021)"),
#    #(209, "C3 Sprint 5 (Nov 29, 2021 - Dec 10, 2021)")
#
#    query_str = "INSERT INTO {} VALUES (?, ?)".format(MILESTONES_TABLE_NAME)
#    cur.executemany(query_str, sql_insert_params)

    # ISSUES ####################################

    # DELETE TABLE ##############

    try:
        cur.execute("DROP TABLE {}".format(ISSUES_TABLE_NAME))
    except:
        pass

    # CREATE TABLE ##############

    sql_query_str = """CREATE TABLE {} (
        id               INTEGER,
        state            TEXT,
        title            TEXT,
        description      TEXT,
        labels           TEXT,
        created_at       TEXT,
        updated_at       TEXT,
        milestone_id     INTEGER,
        web_url          TEXT,
        project_id       INTEGER,
        iid              INTEGER,
        num_notes        INTEGER,
        upload_required  INTEGER,
        PRIMARY KEY (id)
    )""".format(ISSUES_TABLE_NAME)

    cur.execute(sql_query_str)

    # FETCH JSON DATA ###########

    sql_insert_params = [
            (
                issue_dict["id"],
                issue_dict["state"],
                issue_dict["title"],
                issue_dict["description"],
                ",".join(issue_dict["labels"]),
                issue_dict["created_at"],
                issue_dict["updated_at"],
                #issue_dict["milestone"]["id"] if ("milestone" in issue_dict and "id" in issue_dict["milestone"]) else "",
                issue_dict["milestone"]["id"] if (issue_dict["milestone"] is not None) else "",
                issue_dict["web_url"],
                issue_dict["project_id"],
                issue_dict["iid"],
                issue_dict["user_notes_count"],
                0,
                ) for issue_dict in issue_list
            ]

    # INSERT SQL DATA ###########

    question_marks = ", ".join(["?" for x in sql_insert_params[0]])
    query_str = "INSERT INTO {} VALUES ({})".format(ISSUES_TABLE_NAME, question_marks)
    cur.executemany(query_str, sql_insert_params)

    # COMMIT ####################################

    con.commit()
    con.close()


def get_last_db_update_datetime():
    # GET THE LAST UPDATE DATE IN THE SQLITE DATABASE #########
    con = sqlite3.connect(SQLITE_FILE_PATH)
    cur = con.cursor()

    cur.execute("SELECT MAX(updated_at) FROM {}".format(ISSUES_TABLE_NAME))
    last_db_update_str = cur.fetchone()[0]
    con.close()

    print("Last DB update:", last_db_update_str)
    return last_db_update_str


def update_sqlite_database(issue_list):
    con = sqlite3.connect(SQLITE_FILE_PATH)
    cur = con.cursor()

    # GET THE LIST OF KNOWN IDS #

    print(issue_list)
    
    known_ids = []
    for row in cur.execute('SELECT id FROM {}'.format(ISSUES_TABLE_NAME)):
        known_ids.append(row[0])

    # SPLIT issue_list ##########

    issues_to_insert_list = []
    issues_to_update_list = []

    for issue_dict in issue_list:
        if issue_dict["id"] in known_ids:
            issues_to_update_list.append(issue_dict)
        else:
            issues_to_insert_list.append(issue_dict)

    print("- issues_to_insert_list", len(issues_to_insert_list))
    print("- issues_to_update_list", len(issues_to_update_list))

    # INSERT SQL DATA ###########

    if len(issues_to_insert_list) > 0:
        sql_insert_params = [
                (
                    issue_dict["id"],
                    issue_dict["state"],
                    issue_dict["title"],
                    issue_dict["description"],
                    ",".join(issue_dict["labels"]),
                    issue_dict["created_at"],
                    issue_dict["updated_at"],
                    #issue_dict["milestone"]["id"] if ("milestone" in issue_dict and "id" in issue_dict["milestone"]) else "",
                    issue_dict["milestone"]["id"] if (issue_dict["milestone"] is not None) else "",
                    issue_dict["web_url"],
                    issue_dict["project_id"],
                    issue_dict["iid"],
                    issue_dict["user_notes_count"],
                    0,
                    ) for issue_dict in issues_to_insert_list
                ]

        question_marks = ", ".join(["?" for x in sql_insert_params[0]])
        cur.executemany("INSERT INTO {} VALUES ({})".format(ISSUES_TABLE_NAME), sql_insert_params, question_marks)

    # UPDATE SQL DATA ###########

    if len(issues_to_update_list) > 0:
        sql_update_params = [
                (
                    issue_dict["id"],
                    issue_dict["state"],
                    issue_dict["title"],
                    issue_dict["description"],
                    ",".join(issue_dict["labels"]),
                    issue_dict["created_at"],
                    issue_dict["updated_at"],
                    #issue_dict["milestone"]["id"] if ("milestone" in issue_dict and "id" in issue_dict["milestone"]) else "",
                    issue_dict["milestone"]["id"] if (issue_dict["milestone"] is not None) else "",
                    issue_dict["web_url"],
                    issue_dict["project_id"],
                    issue_dict["iid"],
                    issue_dict["user_notes_count"],
                    0,
                    issue_dict["id"]
                    ) for issue_dict in issues_to_update_list
                ]

        SQL_UPDATE_QUERY = """UPDATE {} SET
            id=?,
            state=?,
            title=?,
            description=?,
            labels=?,
            created_at=?,
            updated_at=?,
            milestone_id=?,
            web_url=?,
            project_id=?,
            iid=?,
            num_notes=?,
            upload_required=?
            WHERE id=?""".format(ISSUES_TABLE_NAME)

        cur.executemany(SQL_UPDATE_QUERY, sql_update_params)

    con.commit()
    con.close()


def put_request(put_url, data_dict):
    """
    Update issues on GitLab.

    Parameters
    ----------
    put_url : [type]
        [description]
    data_dict : [type]
        [description]

    Returns
    -------
    [type]
        [description]

    Raises
    ------
    Exception
        [description]
    """
    # https://docs.gitlab.com/ee/api/#request-payload
    resp = requests.put(put_url, json=data_dict, headers=HEADER_DICT)

    if resp.status_code != 200:
        raise Exception("Error:" + resp.text)

    json_dict = json.loads(resp.text)
    return json_dict


def post_request(post_url, data_dict):
    """
    Post new issues on GitLab.

    Parameters
    ----------
    post_url : [type]
        [description]
    data_dict : [type]
        [description]

    Returns
    -------
    [type]
        [description]

    Raises
    ------
    Exception
        [description]
    """
    # https://docs.gitlab.com/ee/api/issues.html#new-issue
    resp = requests.post(post_url, json=data_dict, headers=HEADER_DICT)

    if resp.status_code != 201:
        raise Exception("Error:" + resp.text)

    json_dict = json.loads(resp.text)
    return json_dict


class IssuesTableModel(QSqlRelationalTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        read_only_columns = (
            "state",
            "title",
            "description",
            "labels",
            "milestone_id",
            "upload_required",
            "num_notes"
        )

        self.read_only_columns_index = (self.fieldIndex(columns_name) for columns_name in read_only_columns)


    def flags(self, index):
        """Returns the item flags for the given `index`.

        See Also
        --------
        - http://doc.qt.io/qt-5/qabstractitemmodel.html#flags
        - http://doc.qt.io/qt-5/qt.html#ItemFlag-enum

        Parameters
        ----------
        index : QModelIndex
            TODO

        Returns
        -------
        ItemFlags
            The item flags for the given `index`.
        """
        if index.column() in self.read_only_columns_index:
            return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled


###############################################################################


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:

    error
        tuple (exctype, value, traceback.format_exc())
    
    finished
        No data

    progress
        int indicating % progress
    '''
    error = Signal(tuple)
    finished = Signal()
    progress = Signal(int)


class Worker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    '''

    def __init__(self, project_iid_list=None, update_after=None):
        super(Worker, self).__init__()
        self.project_iid_list = project_iid_list
        self.update_after = update_after
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            if self.project_iid_list is not None:
                issue_list = fetch_selected_issues(self.project_iid_list, progress_callback=self.signals.progress)
                update_sqlite_database(issue_list)
            elif self.update_after is not None:
                last_db_update_str = get_last_db_update_datetime()       # TODO: THIS IS WRONG BECAUSE OF PUSH AND SELECTIVE PULL !!!
                issue_list = fetch_issues(update_after=last_db_update_str, progress_callback=self.signals.progress)
                update_sqlite_database(issue_list)
            else:
                issue_list = fetch_issues(progress_callback=self.signals.progress)
                make_sqlite_database(issue_list)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()      # Done


###############################################################################

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GitLab Board Mg')
        self.statusBar().showMessage("Ready", 2000)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum {} threads".format(self.threadpool.maxThreadCount()))

        # Make widgets ####################################

        self.tabs = QTabWidget(parent=self)
        self.setCentralWidget(self.tabs)

        # Add tabs
        self.issues_tab = IssuesTab(parent=self.tabs)
        self.tabs.addTab(self.issues_tab, "Issues")

        # SHOW ############################################

        self.showMaximized()

class IssuesTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.tabs = parent
        self.main_window = parent.parentWidget()

        # OPEN THE DATABASE ###############################

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(SQLITE_FILE_PATH)
        assert self.db.open()

        # MAKE WIDGETS ####################################

        filter_hbox = QHBoxLayout()
        batch_processing_hbox = QHBoxLayout()

        # Filters widgets #############

        title_desc_filter_label = QLabel("Contains:", self)

        self.title_desc_filter_edit = QLineEdit()
        self.title_desc_filter_edit.setPlaceholderText("Filter text (on title and description)")

        state_filter_label = QLabel("State:", self)

        self.state_filter_combobox = QComboBox()
        self.state_filter_combobox.addItems(["*", "opened", "closed"])

        milestone_filter_label = QLabel("Milestone:", self)

        self.milestone_filter_combobox = QComboBox()
        self.milestone_filter_combobox.addItems(["*", "Meta"] + list(MILESTONES_DICT.keys()))

        ft_filter_label = QLabel("FT:", self)

        self.ft_filter_combobox = QComboBox()
        self.ft_filter_combobox.addItems(["*", "FT IA", "FT Data", "FT Ops", "FT Scale", "FT Perf"])

        open_board_button = QPushButton('Open', parent=self)
        open_board_button.clicked.connect(self.open_board_action_callback)

        filter_hbox.addWidget(title_desc_filter_label)
        filter_hbox.addWidget(self.title_desc_filter_edit)
        filter_hbox.addWidget(state_filter_label)
        filter_hbox.addWidget(self.state_filter_combobox)
        filter_hbox.addWidget(milestone_filter_label)
        filter_hbox.addWidget(self.milestone_filter_combobox)
        filter_hbox.addWidget(ft_filter_label)
        filter_hbox.addWidget(self.ft_filter_combobox)
        filter_hbox.addWidget(open_board_button)

        # Batch processing widgets ####

        state_bp_label = QLabel("State:", self)
        #state_bp_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        state_bp_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.state_bp_combobox = QComboBox()
        self.state_bp_combobox.addItems(["", "opened", "closed"])

        milestone_bp_label = QLabel("Milestone:", self)
        milestone_bp_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.milestone_bp_combobox = QComboBox()
        self.milestone_bp_combobox.addItems([""] + list(MILESTONES_DICT.keys()))

        board_list_bp_label = QLabel("Board list:", self)
        board_list_bp_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.board_list_bp_combobox = QComboBox()
        self.board_list_bp_combobox.addItems(["", "Longue durée", "Backlog", "En cours/dev", "Bloqué", "Staging/Test", "Prodable", "Déployée/Fini"])  # TODO

        weight_bp_label = QLabel("Weight:", self)
        weight_bp_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.weight_bp_combobox = QComboBox()
        self.weight_bp_combobox.addItems(["", "opened", "closed"])

        assignee_bp_label = QLabel("Assignee:", self)
        assignee_bp_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.assignee_bp_combobox = QComboBox()
        self.assignee_bp_combobox.addItems(["", "Charbel", "Cécile", "Cyril", "Guillaume", "Jérémie", "Marc-Arthur", "Nicolas", "Pierre"])  # TODO

        bp_button = QPushButton('Batch Processing', parent=self)
        bp_button.clicked.connect(self.batch_processing_button_callback)

        batch_processing_hbox.addWidget(state_bp_label)
        batch_processing_hbox.addWidget(self.state_bp_combobox)

        batch_processing_hbox.addWidget(milestone_bp_label)
        batch_processing_hbox.addWidget(self.milestone_bp_combobox)

        batch_processing_hbox.addWidget(board_list_bp_label)
        batch_processing_hbox.addWidget(self.board_list_bp_combobox)

        batch_processing_hbox.addWidget(weight_bp_label)
        batch_processing_hbox.addWidget(self.weight_bp_combobox)

        batch_processing_hbox.addWidget(assignee_bp_label)
        batch_processing_hbox.addWidget(self.assignee_bp_combobox)

        batch_processing_hbox.addWidget(bp_button)

        # Splitter ####################

        splitter = QSplitter(orientation=Qt.Vertical, parent=self)
        self.table_view = QTableView(parent=splitter)
        splitter.addWidget(self.table_view)

        self.description_widget = QPlainTextEdit(splitter)
        splitter.addWidget(self.description_widget)
        ##set_mapped_widgets_enabled(False)
        #self.description_widget.setPlainText("")
        #self.description_widget.setPlaceholderText("")
        #self.description_widget.setDisabled(True)

        # Sync widget #################

        sync_hbox = QHBoxLayout()

        init_db_button = QPushButton('Init', parent=self)
        init_db_button.clicked.connect(self.init_db_callback)

        pull_selected_issues_button = QPushButton('Pull Selected', parent=self)
        pull_selected_issues_button.clicked.connect(self.pull_selected_issues_callback)

        pull_button = QPushButton('Pull', parent=self)
        pull_button.clicked.connect(self.pull_updates_callback)

        push_button = QPushButton('Push', parent=self)
        push_button.clicked.connect(self.push_updates_callback)

        sync_hbox.addWidget(init_db_button)
        sync_hbox.addWidget(pull_selected_issues_button)
        sync_hbox.addWidget(pull_button)
        sync_hbox.addWidget(push_button)

        # SET THE LAYOUT ##################################

        vbox = QVBoxLayout()

        vbox.addLayout(filter_hbox)
        vbox.addLayout(batch_processing_hbox)
        vbox.addWidget(splitter)
        vbox.addLayout(sync_hbox)

        self.setLayout(vbox)

        #############################

        self.model = IssuesTableModel()
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
        self.model.setHeaderData(self.model.fieldIndex("num_notes"), Qt.Horizontal, "#Notes")
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
        self.table_view.setColumnWidth(self.model.fieldIndex("labels"), 350)
        self.table_view.setColumnWidth(self.model.fieldIndex("iid"), 35)
        self.table_view.setColumnWidth(self.model.fieldIndex("num_notes"), 50)
        self.table_view.setColumnWidth(self.model.fieldIndex("upload_required"), 25)

        # SET QDATAWIDGETMAPPER ###########################

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)          # WARNING: do not use `self.table_source_self.model` here otherwise the index mapping will be wrong!
        self.mapper.addMapping(self.description_widget, self.model.fieldIndex("description"))

        # https://doc.qt.io/qtforpython/examples/example_sql__books.html
        selection_model = self.table_view.selectionModel()
        selection_model.currentRowChanged.connect(self.mapper.setCurrentModelIndex)

        self.table_view.setCurrentIndex(self.model.index(0, 0))
        #self.self.mapper.toFirst()                      # TODO: is it a good idea ?

        #self.table_view.selectionModel().selectionChanged.connect(self.update_selection)

        # TODO: http://doc.qt.io/qt-5/qdatawidgetmapper.html#setCurrentModelIndex
        #self.self.table_view.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex())

        # TODO: https://doc-snapshots.qt.io/qtforpython/PySide2/QtWidgets/QDataWidgetMapper.html#PySide2.QtWidgets.PySide2.QtWidgets.QDataWidgetMapper.setCurrentModelIndex
        #connect(myTableView.selectionModel(), SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"),
        #mapper, SLOT(setCurrentModelIndex(QModelIndex)))

        # CONNECT CALLBACKS ###############################

        self.model.dataChanged.connect(self.data_changed_callback)                # TODO
        self.title_desc_filter_edit.textChanged.connect(self.filter_callback)
        self.state_filter_combobox.currentIndexChanged.connect(self.filter_callback)
        self.milestone_filter_combobox.currentIndexChanged.connect(self.filter_callback)
        self.ft_filter_combobox.currentIndexChanged.connect(self.filter_callback)

        # DEFINE ACTIONS AND SHORTCUT KEYS ################

        # Open web page action
        open_issue_action = QAction(self.table_view)
        open_issue_action.setShortcut(Qt.CTRL | Qt.Key_Space)

        open_issue_action.triggered.connect(self.open_issue_action_callback)
        self.table_view.addAction(open_issue_action)

        # Open board web page action
        open_board_action = QAction(self.table_view)
        open_board_action.setShortcut(Qt.CTRL | Qt.Key_B)

        open_board_action.triggered.connect(self.open_board_action_callback)
        self.table_view.addAction(open_board_action)

        ## Push action
        # TODO: pour le moment, qd on fait ctrl+s, ça écrase les modifs en cours dans le widget "description" car tant qu'on est pas sorti du widget description les changements ne sont pas enregistrés dans le model et donc ne sont pas poussés (et pour une raison inconnue les modifs en cours sont perdues) => il faut au tout début de l'action push enregistrer le contenu actuel du widget dans le model !!!
        #push_action = QAction(self.table_view)
        #push_action.setShortcut(Qt.CTRL | Qt.Key_S)

        #push_action.triggered.connect(self.push_updates_callback)
        #self.table_view.addAction(push_action)

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

        # Fix encoding
        fix_encoding_action = QAction(self.table_view)
        fix_encoding_action.setShortcut(Qt.CTRL | Qt.Key_F)
        fix_encoding_action.triggered.connect(self.fix_encoding_callback)
        self.table_view.addAction(fix_encoding_action)

        # DEFAULT FILTERS #################################

        # This has to be set *after* these statements: `self.state_***.currentIndexChanged.connect(self.filter_callback)`...

        self.state_filter_combobox.setCurrentText("opened")
        self.milestone_filter_combobox.setCurrentText([key for key, value in MILESTONES_DICT.items() if value == CURRENT_MILESTONE_ID][0])
        self.ft_filter_combobox.setCurrentText("FT IA")

        self.table_view.sortByColumn(self.model.fieldIndex("title"), Qt.AscendingOrder)


    def data_changed_callback(self, topLeft, bottomRight):
        # TODO: DIRTY WORKAROUND -> SHOULD USE DELEGATES INSTEAD!!!
        # - empecher les appels en boucle causé par le changement de la colonne "update_required"
        # - ce callback ne doit être executé que si le changement vient de la vue (le TableView), pas du backend (i.e. GitLab)
        # => il faut probablement plutôt utiliser le Delegate pour ça...
        print("CHANGED:", topLeft, bottomRight)
        row_index = topLeft.row()      # TODO: DIRTY WORKAROUND
        col_index = topLeft.column()   # TODO: DIRTY WORKAROUND
        if col_index != self.model.fieldIndex("upload_required"):
            self.model.setData(self.model.index(row_index, self.model.fieldIndex("upload_required")), 1)
            self.model.submitAll()  # When you’re finished changing a record, you should always call submitAll() to ensure that the changes are written to the database


    def batch_processing_button_callback(self):
        state_str = self.state_bp_combobox.currentText().strip()
        milestone_str = self.milestone_bp_combobox.currentText().strip()
        board_list_str = self.board_list_bp_combobox.currentText().strip()

        if (state_str != "") or (milestone_str != "") or (board_list_str != ""):
            selection_index_list = self.table_view.selectionModel().selectedRows()
            selected_row_list = [source_index.row() for source_index in selection_index_list]

            if len(selected_row_list) > PUSH_NUM_ROWS_ALERT_THRESHOLD:
                # Add a dialog box to confirm the operation (and show the number of rows concerned)
                title = "{} issues will be updated.".format(len(selected_row_list))
                msg = "Do you want to proceed anyway?"

                msgBox = QMessageBox()
                msgBox.setText(title)
                msgBox.setInformativeText(msg)
                msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
                msgBox.setDefaultButton(QMessageBox.Cancel)
                reply = msgBox.exec()

                if reply == QMessageBox.Cancel:
                    return

            for row_index in sorted(selected_row_list, reverse=True):
                if state_str != "":
                    self.model.setData(self.model.index(row_index, self.model.fieldIndex("state")), state_str)
                if milestone_str != "":
                    print("***", MILESTONES_DICT[milestone_str])
                    self.model.setData(self.model.index(row_index, self.model.fieldIndex("milestone_id")), MILESTONES_DICT[milestone_str])
                if board_list_str != "":
                    pass
                    #self.model.setData(self.model.index(row_index, self.model.fieldIndex("board_list")), board_list_str)     # TODO

                self.model.setData(self.model.index(row_index, self.model.fieldIndex("upload_required")), 1)

            self.model.submitAll()  # When you’re finished changing a record, you should always call submitAll() to ensure that the changes are written to the database
            self.model.select()

        self.state_bp_combobox.setCurrentText("")
        self.milestone_bp_combobox.setCurrentText("")
        self.board_list_bp_combobox.setCurrentText("")


    def progress_callback(self, percent_progress):
        msg = "{}%".format(percent_progress)
        print(msg)
        self.main_window.statusBar().showMessage(msg, 5000)

    def thread_complete_callback(self):
        self.model.select()   # Update the model (and the view)
        # TODO: update the description widget

        msg = "Finished"
        print(msg)
        self.main_window.statusBar().showMessage(msg, 2000)


    def init_db_callback(self):
        worker = Worker()
        worker.signals.progress.connect(self.progress_callback)
        worker.signals.finished.connect(self.thread_complete_callback)

        # Execute
        self.main_window.threadpool.start(worker)


    def pull_selected_issues_callback(self):
        selection_index_list = self.table_view.selectionModel().selectedRows()
        selected_row_list = [source_index.row() for source_index in selection_index_list]

        project_iid_list = []

        if len(selected_row_list) > PUSH_NUM_ROWS_ALERT_THRESHOLD:
            # Add a dialog box to confirm the operation (and show the number of rows concerned)
            title = "{} issues will be updated on GitLab.".format(len(selected_row_list))
            msg = "Do you want to proceed anyway?"

            msgBox = QMessageBox()
            msgBox.setText(title)
            msgBox.setInformativeText(msg)
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            reply = msgBox.exec()

            if reply == QMessageBox.Cancel:
                return

        for row_index in sorted(selected_row_list, reverse=True):
            # Remove rows one by one to allow the removal of non-contiguously selected rows (e.g. "rows 0, 2 and 3")
            
            #print(self.model.index(row_index, self.model.fieldIndex("id")).data(Qt.EditRole), self.model.record(row_index).value("id"))
            record = self.model.record(row_index)

            project_id = record.value("project_id")
            iid = record.value("iid")

            project_iid_list.append((project_id, iid)) 


        worker = Worker(project_iid_list=project_iid_list)
        worker.signals.progress.connect(self.progress_callback)
        worker.signals.finished.connect(self.thread_complete_callback)

        # Execute
        self.main_window.threadpool.start(worker)


    def pull_updates_callback(self): # TODO: last update date may be wrong because of "push" and because of "pull_selected_issues" !!!
        worker = Worker(update_after=True)
        worker.signals.progress.connect(self.progress_callback)
        worker.signals.finished.connect(self.thread_complete_callback)

        # Execute
        self.main_window.threadpool.start(worker)


    def fix_encoding_callback(self):
        selection_index_list = self.table_view.selectionModel().selectedRows()
        selected_row_list = [source_index.row() for source_index in selection_index_list]

        for row_index in sorted(selected_row_list, reverse=True):
            record = self.model.record(row_index)

            description_str = record.value("description")
            title_str = record.value("title")
            labels_str = record.value("labels")

            self.model.setData(self.model.index(row_index, self.model.fieldIndex("description")), description_str.encode("cp1252").decode("utf-8"))
            self.model.setData(self.model.index(row_index, self.model.fieldIndex("title")), title_str.encode("cp1252").decode("utf-8"))
            self.model.setData(self.model.index(row_index, self.model.fieldIndex("labels")), labels_str.encode("cp1252").decode("utf-8"))
        
        self.model.submitAll()


    def push_updates_callback(self):
        selection_index_list = self.table_view.selectionModel().selectedRows()
        selected_row_list = [source_index.row() for source_index in selection_index_list]

        if len(selected_row_list) > PUSH_NUM_ROWS_ALERT_THRESHOLD:
            # Add a dialog box to confirm the operation (and show the number of rows concerned)
            title = "{} issues will be updated on GitLab.".format(len(selected_row_list))
            msg = "Do you want to proceed anyway?"

            msgBox = QMessageBox()
            msgBox.setText(title)
            msgBox.setInformativeText(msg)
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            reply = msgBox.exec()

            if reply == QMessageBox.Cancel:
                return

        for row_index in sorted(selected_row_list, reverse=True):
            # Remove rows one by one to allow the removal of non-contiguously selected rows (e.g. "rows 0, 2 and 3")
            
            #print(self.model.index(row_index, self.model.fieldIndex("id")).data(Qt.EditRole), self.model.record(row_index).value("id"))
            record = self.model.record(row_index)

            issue_id = record.value("id")
            description_str = record.value("description")
            title_str = record.value("title")
            labels_str = record.value("labels")
            state_str = record.value("state")
            milestone_id = record.value("milestone_id")

            data_dict = {
                "title": title_str,
                "description": description_str,
                "labels": labels_str,
                "state": state_str,
                "milestone_id": milestone_id
            }

            if issue_id >= 0:   # UPDATE AN EXISTING ISSUE ON THE REMOTE DATABASE ('PUT' REQUEST)
                issue_iid = record.value("iid")
                project_id = record.value("project_id")

                put_url = GITLAB_HOST + "/api/v4/projects/{}/issues/{}".format(project_id, issue_iid)
                json_dict = put_request(put_url, data_dict)
                print("PUT:", json_dict)
            else:               # CREATE NEW ISSUE ON THE REMOTE DATABASE ('POST' REQUEST)
                post_url = GITLAB_HOST + "/api/v4/projects/{}/issues".format(DEFAULT_PROJECT_ID)
                json_dict = post_request(post_url, data_dict)
                print("POST:", json_dict)

                # UPDATE LOCAL DB WITH THE API RESPONSE
                issue_actual_id = json_dict["id"]
                issue_created_at = json_dict["created_at"]
                issue_updated_at = json_dict["updated_at"]
                issue_web_url = json_dict["web_url"]
                issue_iid = json_dict["iid"]

                #record.setValue("id", issue_actual_id)
                #record.setValue("created_at", issue_created_at)
                #record.setValue("updated_at", issue_updated_at)
                #record.setValue("web_url", issue_web_url)
                #record.setValue("iid", issue_iid)
                self.model.setData(self.model.index(row_index, self.model.fieldIndex("id")), issue_actual_id)
                self.model.setData(self.model.index(row_index, self.model.fieldIndex("created_at")), issue_created_at)
                self.model.setData(self.model.index(row_index, self.model.fieldIndex("updated_at")), issue_updated_at)
                self.model.setData(self.model.index(row_index, self.model.fieldIndex("web_url")), issue_web_url)
                self.model.setData(self.model.index(row_index, self.model.fieldIndex("iid")), issue_iid)

            # UPDATE THE "upload_required" flag
            #record.setValue("upload_required", 0)
            self.model.setData(self.model.index(row_index, self.model.fieldIndex("upload_required")), 0)

            #self.model.setRecord(row_index, record)    # TODO: it doesn't work ???!!!

        self.model.submitAll()  # When you’re finished changing a record, you should always call submitAll() to ensure that the changes are written to the database
        #self.model.select()


    def filter_callback(self):
        title_desc_filter_str = self.title_desc_filter_edit.text()
        state_filter_str = self.state_filter_combobox.currentText()
        milestone_filter_str = self.milestone_filter_combobox.currentText()
        ft_filter_str = self.ft_filter_combobox.currentText()

        global_filter_list = []

        if title_desc_filter_str != '':
            global_filter_list.append("(title LIKE '{}' OR description LIKE '{}')".format('%' + title_desc_filter_str + '%', '%' + title_desc_filter_str + '%'))
        if state_filter_str != '*':
            global_filter_list.append("state = '{}'".format(state_filter_str))
        if milestone_filter_str != '*':
            if milestone_filter_str == 'Meta':
                global_filter_list.append(r"labels LIKE '%Meta%'")
            else:
                global_filter_list.append("milestone_id = {}".format(MILESTONES_DICT[milestone_filter_str]))
        if ft_filter_str == 'FT IA':
            global_filter_list.append(r"labels LIKE '%FT::IA%'")
        if ft_filter_str == 'FT Data':
            global_filter_list.append(r"labels LIKE '%FT::Data%'")
        if ft_filter_str == 'FT Ops':
            global_filter_list.append(r"labels LIKE '%FT::Ops%'")
        if ft_filter_str == 'FT Scale':
            global_filter_list.append(r"labels LIKE '%FT::Scale%'")
        if ft_filter_str == 'FT Perf':
            global_filter_list.append(r"labels LIKE '%FT::Perf%'")

        global_filter_str = "" if len(global_filter_list) == 0 else " AND ".join(global_filter_list)
        self.model.setFilter(global_filter_str)

        print(global_filter_str)


    def open_issue_action_callback(self):
        """
        Display selected issues on GitLab with the default web browser. 
        """
        # See https://doc.qt.io/qt-5/qsqltablemodel.html#removeRows
        # See https://doc.qt.io/qtforpython/overviews/sql-model.html#using-the-sql-model-classes
        # See http://doc.qt.io/qt-5/model-view-programming.html#handling-selections-in-item-views

        selection_index_list = self.table_view.selectionModel().selectedRows()
        selected_row_list = [source_index.row() for source_index in selection_index_list]

        for row_index in sorted(selected_row_list):
            web_url = self.model.index(row_index, self.model.fieldIndex("web_url")).data()     # TODO
            print(web_url)
            webbrowser.open(web_url)


    def open_board_action_callback(self):
        """
        Display selected board on GitLab with the default web browser. 
        """
        # See https://doc.qt.io/qt-5/qsqltablemodel.html#removeRows
        # See https://doc.qt.io/qtforpython/overviews/sql-model.html#using-the-sql-model-classes
        # See http://doc.qt.io/qt-5/model-view-programming.html#handling-selections-in-item-views

        title_desc_filter_str = self.title_desc_filter_edit.text()
        title_desc_filter_str = urllib.parse.quote(title_desc_filter_str)     # urlencodé

        milestone_filter_str = self.milestone_filter_combobox.currentText()

        ft_filter_str = self.ft_filter_combobox.currentText()
        ft_filter_str = ft_filter_str.replace(" ", "::")
        ft_filter_str = ft_filter_str.replace("*", "")
        ft_filter_str = urllib.parse.quote(ft_filter_str)     # urlencodé

        if milestone_filter_str == "Meta":
            web_url = "{}/groups/accenta/-/boards?scope=all&label_name[]={}&search={}".format(GITLAB_HOST, "Meta", title_desc_filter_str)    # TODO
        else:
            milestone_filter_str = MILESTONES_DICT2[milestone_filter_str]       # TODO: DIRTY WORKAROUND !
            milestone_filter_str = urllib.parse.quote(milestone_filter_str)     # urlencodé

            web_url = "{}/groups/accenta/-/boards?scope=all&label_name[]={}&milestone_title={}&search={}".format(GITLAB_HOST, ft_filter_str, milestone_filter_str, title_desc_filter_str)    # TODO
            #&milestone_title=C3%20Sprint%203    # TODO: ajouter le milestone dans la ligne ci-dessus... ce qui nécessite de récupérer le "vrai nom" du milestone (celui sur Gitlab)... on ne peut pas utiliser l'ID...

        print("OPEN:", web_url)
        webbrowser.open(web_url)


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
        new_record.setValue("project_id", DEFAULT_PROJECT_ID)
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

    window = MainWindow()

    # The mainloop of the application. The event handling starts from this point.
    exit_code = app.exec()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)