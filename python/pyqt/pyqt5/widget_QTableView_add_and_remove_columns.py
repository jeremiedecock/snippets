#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref:
# - http://doc.qt.io/qt-5/qabstracttablemodel.html#subclassing
# - http://doc.qt.io/qt-5/qabstractitemmodel.html#insertColumns
# - http://doc.qt.io/qt-5/qabstractitemmodel.html#beginInsertColumns

import random
import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QPushButton, QVBoxLayout


class MyData:
    def __init__(self):
        self._data = [[], []]

    def get_num_rows(self):
        return 2

    def get_num_columns(self):
        return len(self._data[0])

    def get_data(self, row_index, column_index):
        value = self._data[row_index][column_index]
        return value

    def insert_column(self, index):
        for row in self._data:
            row.insert(index, str(random.randint(0, 9)))

    def remove_column(self, index):
        if len(self._data[0]) > 0:
            for row in self._data:
                _removed = row.pop(index)

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

    def insertColumns(self, column, count, parent):
        """
        On models that support this, inserts count columns into the model before the given column.
        Items in the new column will be children of the item represented by the parent model index.

        If column is 0, the columns are prepended to any existing columns in the parent.

        If column is columnCount(), the columns are appended to any existing columns in the parent.

        If parent has no children, a single column with count columns is inserted.

        Returns true if the columns were successfully inserted; otherwise returns false.

        If you implement your own model, you can reimplement this function if you want to support insertions.
        Alternatively, you can provide your own API for altering the data.
        In either case, you will need to call beginInsertColumns() and endInsertColumns() to notify other components that the
        model has changed.
        """
        parent = parent
        first_index = 0
        last_index = first_index + count - 1

        self.beginInsertColumns(parent, first_index, last_index)

        for i in range(count):
            self.data.insert_column(first_index)

        self.endInsertColumns()

    def removeColumns(self, column, count, parent):
        parent = parent
        first_index = 0
        last_index = first_index + count - 1

        self.beginRemoveColumns(parent, first_index, last_index)

        for i in range(count):
            self.data.remove_column(first_index)

        self.endRemoveColumns()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Make widgets

    window = QWidget()

    table_view = QTableView()

    btn_add_column = QPushButton("Add a column")
    btn_remove_column = QPushButton("Remove the first column")

    # Set the layout

    vbox = QVBoxLayout()

    vbox.addWidget(table_view)
    vbox.addWidget(btn_add_column)
    vbox.addWidget(btn_remove_column)

    window.setLayout(vbox)

    # Set models

    data = MyData()
    my_model = MyModel(data)
    table_view.setModel(my_model)

    # Set slots

    def add_column():
        print("add")
        parent = QModelIndex()                # more useful with tree structures for instance
        my_model.insertColumns(0, 1, parent)
        #my_model.insertColumns(0, 2, None)  # Ok, you can try it

    def remove_column():
        print("remove")
        parent = QModelIndex()                # more useful with tree structures for instance
        my_model.removeColumns(0, 1, parent)
        #my_model.removeColumns(0, 2, None)  # Ok, you can try it

    btn_add_column.clicked.connect(add_column)
    btn_remove_column.clicked.connect(remove_column)

    # Show

    window.show()


    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)