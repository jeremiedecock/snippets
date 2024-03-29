#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: http://doc.qt.io/qt-5/modelview.html#2-1-a-read-only-table

import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex
from PyQt5.QtWidgets import QApplication, QTableView

###############################################################################

class MyModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._data = [[0, 0, 0], [0, 0, 0]]   # CAUTION: don't call this "self.data", it's already taken by "self.data(...)"

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._data[0])

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return QVariant()

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value

            # The following line are necessary e.g. to dynamically update the QSortFilterProxyModel
            self.dataChanged.emit(index, index, [Qt.EditRole])

        return True

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled


if __name__ == '__main__':
    app = QApplication(sys.argv)

    table_view = QTableView()
    my_model = MyModel()
    table_view.setModel(my_model)
    table_view.show()

    # GIVE FOCUS TO CELL(1,1) IN EDIT MODE!
    # https://pyqt.riverbankcomputing.narkive.com/mIxVZuAN/how-to-give-focus-to-a-particular-cell-in-qtableview
    index = my_model.index(1, 1)
    table_view.setCurrentIndex(index)
    table_view.edit(index)

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
