#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: http://doc.qt.io/qt-5/qdatawidgetmapper.html#details

import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QVBoxLayout, QSpinBox, QLineEdit, \
    QDataWidgetMapper


class MyData:
    def __init__(self):
        self._num_rows = 3
        self._num_columns = 2

        self._data = [["0", "Hello"] for i in range(self._num_rows)]

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
        if role == Qt.DisplayRole or role == Qt.EditRole:
            # See https://stackoverflow.com/a/8480223
            return self.data.get_data(index.row(), index.column())
        return QVariant()

    def setData(self, index, value, role):
        if role == Qt.EditRole:

            try:
                self.data.set_data(index.row(), index.column(), value)

                # The following line are necessary e.g. to dynamically update the QSortFilterProxyModel
                self.dataChanged.emit(index, index, [Qt.EditRole])
            except Exception as e:
                print(e)
                return False

        return True

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

app = QApplication(sys.argv)

window = QWidget()

data = MyData()

table_view = QTableView()
my_model = MyModel(data)
table_view.setModel(my_model)

spin_box = QSpinBox()
spin_box.setMinimum(-10000)
spin_box.setMaximum(10000)
line_edit = QLineEdit()

vbox = QVBoxLayout()

vbox.addWidget(table_view)
vbox.addWidget(spin_box)
vbox.addWidget(line_edit)

window.setLayout(vbox)

###

mapper = QDataWidgetMapper()        # <--
mapper.setModel(my_model)           # <--
mapper.addMapping(spin_box, 0)      # <--
mapper.addMapping(line_edit, 1)     # <--
mapper.toFirst()                    # <--

def update_selection(selected, deselected):                 # <--
    index = table_view.selectionModel().currentIndex()      # <--
    mapper.setCurrentIndex(index.row())                     # <--
    print("Index: ", index.row())

table_view.selectionModel().selectionChanged.connect(update_selection)   # <--

###

window.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)