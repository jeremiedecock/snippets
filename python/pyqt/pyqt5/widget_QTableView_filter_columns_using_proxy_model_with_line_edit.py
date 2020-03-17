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
from PyQt5.QtWidgets import QApplication, QWidget, QTableView, QLineEdit, QVBoxLayout


class MyModel(QAbstractTableModel):

    def __init__(self, parent):
        super().__init__(parent)

        self.data = np.random.randint(0, 3, (20, 2))

    def rowCount(self, parent):
        return self.data.shape[0]

    def columnCount(self, parent):
        return self.data.shape[1]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return "{}".format(self.data[index.row(), index.column()])

        return QVariant()


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Make widgets #################

        self.edit = QLineEdit()
        self.table_view = QTableView()

        self.edit.setPlaceholderText("Filter text (on col. 1)")

        # Set the layout ############################

        vbox = QVBoxLayout()

        vbox.addWidget(self.edit)
        vbox.addWidget(self.table_view)

        self.setLayout(vbox)

        # Set Model and ProxyModel ##################

        my_model = MyModel(None)

        self.proxy_model = QSortFilterProxyModel()   # <--
        self.proxy_model.setSourceModel(my_model)    # <--
        self.table_view.setModel(self.proxy_model)        # <--
        #self.table_view.setModel(my_model)

        #self.proxy_model.setFilterRegExp(QRegExp("1", Qt.CaseInsensitive, QRegExp.FixedString))     # <--
        self.proxy_model.setFilterKeyColumn(0)                                                      # <--
        #self.table_view.setSortingEnabled(True)

        # Set LineEdit slot #########################

        self.edit.textChanged.connect(self.foo)


    def foo(self):
        filter_str = self.edit.text()
        self.proxy_model.setFilterRegExp(QRegExp(filter_str, Qt.CaseInsensitive, QRegExp.FixedString))     # <--


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
