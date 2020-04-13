#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: http://doc.qt.io/qt-5/modelview.html#2-1-a-read-only-table

import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, QTimer, QVariant
from PyQt5.QtWidgets import QApplication, QTableView

###############################################################################

class MyModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._data = [[0, 0], [0, 0]]   # CAUTION: don't call this "self.data", it's already taken by "self.data(...)"

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._data[0])

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value

            # The following line are necessary e.g. to dynamically update the QSortFilterProxyModel
            self.dataChanged.emit(index, index, [Qt.EditRole])

        return True

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

cpt = 0

def timerHit():
    global cpt
    cpt += 1

    index = my_model.index(0, 0)   # Top left cell
    my_model.setData(index, str(cpt), Qt.EditRole)
    print(my_model.data(index, Qt.DisplayRole))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    table_view = QTableView()
    my_model = MyModel()
    table_view.setModel(my_model)
    table_view.show()

    timer = QTimer()
    timer.timeout.connect(timerHit)
    timer.start(1000)

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
