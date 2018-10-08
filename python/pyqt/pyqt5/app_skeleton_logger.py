#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation:
# - http://doc.qt.io/qt-5/modelview.html
# - http://doc.qt.io/qt-5/model-view-programming.html

# TODO:
# - [x] Keep the current value while editing a cell -> see https://stackoverflow.com/a/8480223
# -
# - [x] Remove selected lines instead of the last one TODO: check the possible (but very unlikely bug) when reomving non-contiguous rows
# - [+] Remove using the "Suppr" key instead of a button -> simply call the remove_rows callback when the suppr key is pressed...
# - Add a keyboard shortcut to add a row
# - [+] Sort by datetime or by value. See http://doc.qt.io/qt-5/model-view-programming.html#sorting , http://doc.qt.io/qt-5/qsortfilterproxymodel.html#sorting and https://stackoverflow.com/questions/11606259/how-to-sort-a-qtableview-by-a-column#11606946
# -
# - [+] Use Qt delegate example
# - [+] Don't show all Model's columns (+ add a description column in the model but don't show it in the view): "table_view.setColumnHidden(column_num, True)"
# - [+] Use QDataWidgetMapper example (with the hidden description column for instance)
# -
# - [+] Add Tabs widgets + add a matplotlib plot of values
# - [+] Add "undo" and "redo" actions (search "(python) design pattern for undo redo actions") -> Command pattern and Memento pattern (https://stackoverflow.com/a/3448959)
# - Add doc strings
# -
# - When a row is inserted, select it (+ auto scroll to it) + automatically edit its first value column
# - Use a system date time dialog box to edit date time (with calendar and clock...)
# - Improve the architecture: merge DataWrapper and IO module functions ?

import copy
import datetime
import fcntl
import os
import sys

from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QPushButton, QVBoxLayout, QMainWindow

HOME_PATH = os.path.expanduser("~")                 # TODO: works on Unix only ?
FILE_NAME = ".logger_skeleton"
FILE_PATH = os.path.join(HOME_PATH, FILE_NAME)
LOCK_PATH = FILE_PATH + ".lock"

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# I/O MODULE ##################################################################

DEFAULT_DATA = []                             # TODO ?

IO_FORMAT = "json"
#IO_FORMAT = "yaml"
#IO_FORMAT = "csv"
#IO_FORMAT = "npy"

def load_data(file_path):
    if os.path.isfile(file_path):
        if IO_FORMAT == "json":
            raw_data = load_data_json(file_path)
        elif IO_FORMAT == "yaml":
            raw_data = load_data_yaml(file_path)
        else:
            raise ValueError("Unknown IO format: {}".format(IO_FORMAT))
    else:
        # Make default data if file doesn't exist
        raw_data = DEFAULT_DATA

    data = DataWrapper(raw_data)              # TODO ?

    return data

def save_data(data, file_path):
    raw_data = data._data                     # TODO ?

    if IO_FORMAT == "json":
        save_data_json(raw_data, file_path)
    elif IO_FORMAT == "yaml":
        save_data_yaml(raw_data, file_path)
    else:
        raise ValueError("Unknown IO format: {}".format(IO_FORMAT))

# JSON ################################

import json

def load_data_json(file_path):
    with open(file_path, "r") as fd:
        data = json.load(fd)

    for row in data:
        row[0] = datetime.datetime.strptime(row[0], DATE_TIME_FORMAT)

    return data

def save_data_json(data, file_path):
    data = copy.deepcopy(data)

    for row in data:
        row[0] = row[0].strftime(format=DATE_TIME_FORMAT)

    with open(file_path, "w") as fd:
        #json.dump(data, fd)                           # no pretty print
        json.dump(data, fd, sort_keys=True, indent=4)  # pretty print format

# YAML ################################

import yaml

def load_data_yaml(file_path):
    with open(file_path, "r") as fd:
        data = yaml.safe_load(fd)
    return data

def save_data_yaml(data, file_path):
    with open(file_path, 'w') as fd:
        yaml.dump(data, fd)
        #yaml.dump(data, fd, default_flow_style=False)

# CSV #################################

# TODO

# NPY #################################

# TODO

# DATA MODULE #################################################################

class DataWrapper:

    def __init__(self, raw_data):
        self._data = raw_data

        self.headers = ["Date time", "Value"]
        self.default_values = [None, 0]

    def get_num_rows(self):
        return len(self._data)

    def get_num_columns(self):
        return len(self.headers)

    def get_data(self, row_index, column_index):
        value = self._data[row_index][column_index]
        if column_index == 0:
            #value = value.isoformat()
            value = value.strftime(format=DATE_TIME_FORMAT)
        return value

    def set_data(self, row_index, column_index, value):
        #print("write ({},{}): {}".format(row_index, column_index, value))

        try:
            if column_index == 0:
                value = datetime.datetime.strptime(value, DATE_TIME_FORMAT)
            else:
                value = float(value)                      # Expect numerical values here... remove otherwise
            self._data[row_index][column_index] = value
        except Exception as e:
            print(e, file=sys.stderr)
            return False

        return True

    def insert_row(self, index):
        new_row = copy.deepcopy(self.default_values)
        new_row[0] = datetime.datetime.now()
        self._data.insert(index, new_row)

    def remove_row(self, index):
        if self.get_num_rows() > 0:
            _removed = self._data.pop(index)

# GUI MODULE ##################################################################

# MODEL ###############################

class DataQtModel(QAbstractTableModel):

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data

    def rowCount(self, parent):
        return self.data.get_num_rows()

    def columnCount(self, parent):
        return self.data.get_num_columns()

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            # See https://stackoverflow.com/a/8480223
            return self.data.get_data(index.row(), index.column())
        return QVariant()

    def headerData(self, index, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return str(index+1)
            elif orientation == Qt.Horizontal:
                return self.data.headers[index]
        return None

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            returned_value = self.data.set_data(index.row(), index.column(), value)
        return returned_value

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
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

    def insertRows(self, row, count, parent):
        """Inserts `count` rows into the model before the given `row`.

        Items in the new row will be children of the item represented by the `parent` model index.

        If `row` is 0, the rows are prepended to any existing rows in the `parent`.

        If `row` is `rowCount()`, the rows are appended to any existing rows in the `parent`.

        If `parent` has no children, a single column with `count` rows is inserted.

        Returns `True` if the rows were successfully inserted; otherwise returns `False`.

        See Also
        --------
        http://doc.qt.io/qt-5/qabstractitemmodel.html#insertRows

        Parameters
        ----------
        row : int
            TODO
        count : int
            TODO
        parent : QModelIndex, optional
            TODO

        Returns
        -------
        bool
            Returns `True` if the rows were successfully removed; otherwise returns `False`.
        """
        try:
            parent = parent
            first_index = row
            last_index = first_index + count - 1

            self.beginInsertRows(parent, first_index, last_index)

            for i in range(count):
                self.data.insert_row(first_index)

            self.endInsertRows()
        except:
            return False

        return True

    def removeRows(self, row, count, parent):
        """Removes `count` rows starting with the given `row` under parent `parent` from the model.

        See Also
        --------
        http://doc.qt.io/qt-5/qabstractitemmodel.html#removeRows

        Parameters
        ----------
        row : int
            TODO
        count : int
            TODO
        parent : QModelIndex, optional
            TODO

        Returns
        -------
        bool
            Returns `True` if the rows were successfully removed; otherwise returns `False`.
        """
        # See http://doc.qt.io/qt-5/qabstractitemmodel.html#removeRows

        try:
            parent = parent
            first_index = row
            last_index = first_index + count - 1

            self.beginRemoveRows(parent, first_index, last_index)

            for i in range(count):
                self.data.remove_row(first_index)

            self.endRemoveRows()
        except:
            return False

        return True

# VIEW ################################

class Window(QMainWindow):

    def __init__(self, data):
        super().__init__()

        self.resize(400, 600)
        self.setWindowTitle('Logger Skeleton')

        # Make widgets

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.table_view = QTableView()
        self.btn_add_row = QPushButton("Add a row")
        self.btn_remove_row = QPushButton("Remove selected rows")

        # Set the layout

        vbox = QVBoxLayout()

        vbox.addWidget(self.table_view)
        vbox.addWidget(self.btn_add_row)
        vbox.addWidget(self.btn_remove_row)

        central_widget.setLayout(vbox)

        # Set models

        my_model = DataQtModel(data)
        self.table_view.setModel(my_model)
        self.table_view.setColumnWidth(0, 200)                       # TODO: automatically get the best width

        # Set slots

        self.btn_add_row.clicked.connect(self.add_row_btn_callback)
        self.btn_remove_row.clicked.connect(self.remove_row_callback)

        #self.table_view.setColumnHidden(1, True)

        # Show

        self.show()

    def add_row_btn_callback(self):
        parent = QModelIndex()                                   # More useful with e.g. tree structures

        #row_index = 0                                           # Insert new rows to the begining
        row_index = self.table_view.model().rowCount(parent)     # Insert new rows to the end

        self.table_view.model().insertRows(row_index, 1, parent)

    def remove_row_callback(self):
        parent = QModelIndex()                                   # More useful with e.g. tree structures

        # See http://doc.qt.io/qt-5/model-view-programming.html#handling-selections-in-item-views
        #current_index = self.table_view.selectionModel().currentIndex()
        #print("Current index:", current_index.row(), current_index.column())

        selection_index_list = self.table_view.selectionModel().selectedRows()
        selected_row_list = [selection_index.row() for selection_index in selection_index_list]

        print("Current selection:", selected_row_list)

        #row_index = 0                                           # Remove the first row
        #row_index = self.table_view.model().rowCount(parent) - 1 # Remove the last row

        # WARNING: the list of rows to remove MUST be sorted in reverse order
        # otherwise the index of rows to remove may change at each iteration of the for loop!

        # TODO: there should be a lock mechanism to avoid model modifications from external sources while iterating this loop...
        #       Or as a much simpler alternative, modify the ItemSelectionMode to forbid the non contiguous selection of rows and remove the following for loop
        for row_index in sorted(selected_row_list, reverse=True):
            # Remove rows one by one to allow the removql of non-contiguously selected rows (e.g. "rows 0, 2 and 3")
            success = self.table_view.model().removeRows(row_index, 1, parent)
            if not success:
                raise Exception("Unknown error...")   # TODO

# RUN MODULE ##################################################################

def main():

    data = load_data(FILE_PATH)              # TODO ?

    app = QApplication(sys.argv)
    app.setApplicationName("Logger Skeleton")

    # Make widgets
    window = Window(data)

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    save_data(data, FILE_PATH)              # TODO ?

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)


if __name__ == '__main__':

    # Ensure a single instance of an application is running (TODO: check whether it works on MacOS and Windows!)

    print("Acquire an exclusive lock on ", LOCK_PATH)

    fd = open(LOCK_PATH, "w")

    try:
        # LOCK_EX = acquire an exclusive lock on fd
        # LOCK_NB = make a nonblocking request
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

        main()

        # LOCK_UN = unlock fd
        fcntl.flock(fd, fcntl.LOCK_UN)
        print("Unlock ", LOCK_PATH)
    except IOError:
        print(LOCK_PATH + " is locked ; another instance is running. Exit.")
        sys.exit(1)

