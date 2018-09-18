#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtWidgets import QApplication, QTableView

class MyModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)

    def rowCount(self, parent):
        return 3

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str([index.row(), index.column()])
        return None

    def headerData(self, index, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return "ROW {}".format(index)
            elif orientation == Qt.Vertical:
                return "COLUMN {}".format(index)
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)

    table_view = QTableView()
    my_model = MyModel()
    table_view.setModel(my_model)
    table_view.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
