#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref:
# - http://doc.qt.io/qt-5/modelview.html
# - http://doc.qt.io/qt-5/qabstractitemview.html#selectionChanged
# - http://doc.qt.io/qt-5/qitemselection.html
# - http://doc.qt.io/qt-5/qmodelindex.html

import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtWidgets import QApplication, QTableView


class MyModel(QAbstractTableModel):

    def __init__(self, parent):
        super().__init__(parent)

    def rowCount(self, parent):
        return 2

    def columnCount(self, parent):
        return 3

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return "{}{}".format(index.row(), index.column())

        return QVariant()


def print_selection(new_selection, old_selection):
    old_selection_indexes = [((index.row(), index.column()), index.data(Qt.DisplayRole)) for index in old_selection.indexes()]
    new_selection_indexes = [((index.row(), index.column()), index.data(Qt.DisplayRole)) for index in new_selection.indexes()]
    print(old_selection_indexes, " -> ", new_selection_indexes)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    table_view = QTableView()

    my_model = MyModel(None)
    table_view.setModel(my_model)

    # Bind selection to the print_selection function (must be after the model setup)
    selection_model = table_view.selectionModel()
    selection_model.selectionChanged.connect(print_selection)

    table_view.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)