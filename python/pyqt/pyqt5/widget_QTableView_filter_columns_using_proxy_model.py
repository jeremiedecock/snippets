#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref:
# - http://doc.qt.io/qt-5/model-view-programming.html#sorting
# - http://doc.qt.io/qt-5/model-view-programming.html#proxy-models
# - http://doc.qt.io/qt-5/qsortfilterproxymodel.html#sorting
# - https://stackoverflow.com/a/11606946
# - http://doc.qt.io/qt-5/qtwidgets-itemviews-basicsortfiltermodel-example.html
# - http://doc.qt.io/qt-5/qtwidgets-itemviews-customsortfiltermodel-example.html

import numpy as np
import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QSortFilterProxyModel, QRegExp
from PyQt5.QtWidgets import QApplication, QTableView


class MyModel(QAbstractTableModel):

    def __init__(self, parent):
        super().__init__(parent)

        self.data = np.random.randint(0, 3, (20, 3))

    def rowCount(self, parent):
        return self.data.shape[0]

    def columnCount(self, parent):
        return self.data.shape[1]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return "{}".format(self.data[index.row(), index.column()])

        return QVariant()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    table_view = QTableView()
    my_model = MyModel(None)

    proxy_model = QSortFilterProxyModel()   # <--
    proxy_model.setSourceModel(my_model)    # <--
    table_view.setModel(proxy_model)        # <--
    #table_view.setModel(my_model)

    proxy_model.setFilterRegExp(QRegExp("1", Qt.CaseInsensitive, QRegExp.FixedString))     # <--
    proxy_model.setFilterKeyColumn(0)                                                      # <--
    #table_view.setSortingEnabled(True)

    table_view.show()


    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
