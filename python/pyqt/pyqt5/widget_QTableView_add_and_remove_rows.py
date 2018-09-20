#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref:
# - http://doc.qt.io/qt-5/qabstracttablemodel.html#subclassing
# - http://doc.qt.io/qt-5/qabstractitemmodel.html#insertRows
# - http://doc.qt.io/qt-5/qabstractitemmodel.html#beginInsertRows

import random
import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QPushButton, QVBoxLayout


class MyData:
    def __init__(self):
        self._data = []

    def get_num_rows(self):
        return len(self._data)

    def get_num_columns(self):
        return 2

    def get_data(self, row_index, column_index):
        value = self._data[row_index][column_index]
        return value

    def insert_row(self, index):
        row = [str(random.randint(0, 9)) for index in range(self.get_num_columns())]
        self._data.insert(index, row)

    def remove_row(self, index):
        if self.get_num_rows() > 0:
            _removed = self._data.pop(index)

###############################################################################

class MyModel(QAbstractTableModel):

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data

    def rowCount(self, parent):
        return self.data.get_num_rows()

    def columnCount(self, parent):
        return self.data.get_num_columns()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.data.get_data(index.row(), index.column())
        return QVariant()

    def insertRows(self, row, count, parent):
        """
        On models that support this, inserts count rows into the model before the given row.
        Items in the new row will be children of the item represented by the parent model index.

        If row is 0, the rows are prepended to any existing rows in the parent.

        If row is rowCount(), the rows are appended to any existing rows in the parent.

        If parent has no children, a single column with count rows is inserted.

        Returns true if the rows were successfully inserted; otherwise returns false.

        If you implement your own model, you can reimplement this function if you want to support insertions.
        Alternatively, you can provide your own API for altering the data.
        In either case, you will need to call beginInsertRows() and endInsertRows() to notify other components that the
        model has changed.
        """
        parent = parent
        first_index = 0
        last_index = first_index + count - 1

        self.beginInsertRows(parent, first_index, last_index)

        for i in range(count):
            self.data.insert_row(first_index)

        self.endInsertRows()

    def removeRows(self, row, count, parent):
        parent = parent
        first_index = 0
        last_index = first_index + count - 1

        self.beginRemoveRows(parent, first_index, last_index)

        for i in range(count):
            self.data.remove_row(first_index)

        self.endRemoveRows()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Make widgets

    window = QWidget()

    table_view = QTableView()

    btn_add_row = QPushButton("Add a row")
    btn_remove_row = QPushButton("Remove the first row")

    # Set the layout

    vbox = QVBoxLayout()

    vbox.addWidget(table_view)
    vbox.addWidget(btn_add_row)
    vbox.addWidget(btn_remove_row)

    window.setLayout(vbox)

    # Set models

    data = MyData()
    my_model = MyModel(data)
    table_view.setModel(my_model)

    # Set slots

    def add_row():
        print("add")
        parent = QModelIndex()                # more useful with tree structures for instance
        my_model.insertRows(0, 1, parent)
        #my_model.insertRows(0, 2, None)  # Ok, you can try it

    def remove_row():
        print("remove")
        parent = QModelIndex()                # more useful with tree structures for instance
        my_model.removeRows(0, 1, parent)
        #my_model.removeRows(0, 2, None)  # Ok, you can try it

    btn_add_row.clicked.connect(add_row)
    btn_remove_row.clicked.connect(remove_row)

    # Show

    window.show()


    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)