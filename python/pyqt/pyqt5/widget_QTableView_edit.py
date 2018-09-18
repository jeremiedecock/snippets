#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: http://doc.qt.io/qt-5/modelview.html#2-1-a-read-only-table

import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtWidgets import QApplication, QTableView

class MyData:
    def __init__(self):
        self._num_rows = 3
        self._num_columns = 2

        self._data = [["-" for j in range(self._num_columns)] for i in range(self._num_rows)]

    def get_num_rows(self):
        return self._num_rows

    def get_num_columns(self):
        return self._num_columns

    def get_data(self, row_index, column_index):
        value = self._data[row_index][column_index]
        print("read ({},{}): {}".format(row_index, column_index, value))
        return value

    def set_data(self, row_index, column_index, value):
        print("write ({},{}): {}".format(row_index, column_index, value))
        self._data[row_index][column_index] = value

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

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self.data.set_data(index.row(), index.column(), value)
        return True

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

if __name__ == '__main__':
    app = QApplication(sys.argv)

    data = MyData()

    table_view = QTableView()
    my_model = MyModel(data)
    table_view.setModel(my_model)
    table_view.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)