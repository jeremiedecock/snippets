#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: http://doc.qt.io/qt-5/modelview.html#2-1-a-read-only-table

import sys
from datetime import datetime

from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QTimer, QModelIndex
from PyQt5.QtWidgets import QApplication, QTableView

class MyModel(QAbstractTableModel):

    def __init__(self, parent):
        super().__init__(parent)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerHit)
        self.timer.start(1000)

    def timerHit(self):
        top_left_cell = self.index(0, 0)
        self.dataChanged.emit(top_left_cell, top_left_cell)

    def rowCount(self, parent):
        return 2

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.row() == index.column() == 0:
                return str(datetime.now().time())

        return QVariant()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    table_view = QTableView()
    my_model = MyModel(None)
    table_view.setModel(my_model)
    table_view.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
