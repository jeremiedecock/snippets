#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref:
# - http://doc.qt.io/qt-5/modelview.html#3-4-delegates
# - http://doc.qt.io/qt-5/model-view-programming.html#delegate-classes
# - http://doc.qt.io/qt-5/qabstractitemdelegate.html#details
# - http://doc.qt.io/qt-5/qitemdelegate.html#details
# - http://doc.qt.io/qt-5/qstyleditemdelegate.html#details
# - http://doc.qt.io/qt-5/qtwidgets-itemviews-spinboxdelegate-example.html

import sys

from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtWidgets import QApplication, QTableView, QStyledItemDelegate, QSlider


class MyData:
    def __init__(self):
        self._num_rows = 3
        self._num_columns = 2

        self._data = [[0 for j in range(self._num_columns)] for i in range(self._num_rows)]

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
        self._data = data        # DON'T CALL THIS ATTRIBUTE "data", A METHOD ALREADY HAVE THIS NAME (model.data(index, role)) !!!

    def rowCount(self, parent):
        return self._data.get_num_rows()

    def columnCount(self, parent):
        return self._data.get_num_columns()

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            # See https://stackoverflow.com/a/8480223
            return self._data.get_data(index.row(), index.column())
        return QVariant()

    def setData(self, index, value, role):
        if role == Qt.EditRole:

            try:
                self._data.set_data(index.row(), index.column(), value)

                # The following line are necessary e.g. to dynamically update the QSortFilterProxyModel
                self.dataChanged.emit(index, index, [Qt.EditRole])
            except Exception as e:
                print(e)
                return False

        return True

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

###############################################################################

class MyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QSlider(parent=parent, orientation=Qt.Horizontal)
        editor.setRange(0, 5)
        editor.setAutoFillBackground(True)

        editor.setTickPosition(QSlider.TicksBelow)
        editor.setTickInterval(1)

        return editor

    def setEditorData(self, editor, index):
        value = int(index.data(Qt.EditRole))       # equivalent of    value = index.model().data(index, Qt.EditRole)
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        value = editor.value()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    data = MyData()

    table_view = QTableView()
    my_model = MyModel(data)
    table_view.setModel(my_model)

    delegate = MyDelegate()
    table_view.setItemDelegate(delegate)

    table_view.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
