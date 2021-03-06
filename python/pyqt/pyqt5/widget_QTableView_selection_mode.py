#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: http://doc.qt.io/qt-5/modelview.html#2-1-a-read-only-table

import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtWidgets import QApplication, QTableView, QAbstractItemView


class MyModel(QAbstractTableModel):

    def __init__(self, parent):
        super().__init__(parent)

    def rowCount(self, parent):
        return 2

    def columnCount(self, parent):
        return 3

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return "({},{})".format(index.row(), index.column())

        return QVariant()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    table_view = QTableView()
    my_model = MyModel(None)
    table_view.setModel(my_model)

    table_view.setSelectionMode(QAbstractItemView.SingleSelection)       # <- Set selection mode. See http://doc.qt.io/qt-5/qabstractitemview.html#selectionMode-prop
    #table_view.setSelectionMode(QAbstractItemView.ContiguousSelection)  # <- Set selection mode. See http://doc.qt.io/qt-5/qabstractitemview.html#selectionMode-prop
    #table_view.setSelectionMode(QAbstractItemView.ExtendedSelection)    # <- Set selection mode. See http://doc.qt.io/qt-5/qabstractitemview.html#selectionMode-prop
    #table_view.setSelectionMode(QAbstractItemView.MultiSelection)       # <- Set selection mode. See http://doc.qt.io/qt-5/qabstractitemview.html#selectionMode-prop

    table_view.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)