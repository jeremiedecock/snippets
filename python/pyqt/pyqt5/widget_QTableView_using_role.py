#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: http://doc.qt.io/qt-5/modelview.html#2-2-extending-the-read-only-example-with-roles

import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtGui import QFont, QBrush
from PyQt5.QtWidgets import QApplication, QTableView


class MyModel(QAbstractTableModel):

    def __init__(self, parent):
        super().__init__(parent)

    def rowCount(self, parent):
        return 2

    def columnCount(self, parent):
        return 3

    def data(self, index, role):
        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole:
            text = "({},{})".format(row, column)
            return text
        elif role == Qt.FontRole:
            if row == 0 and column == 0:                # change font only for cell(0,0)
                my_font = QFont()
                my_font.setBold(True)
                my_font.setItalic(True)
                my_font.setUnderline(True)
                return my_font
        elif role == Qt.BackgroundRole:
            if row == 1 and column == 2:                # change background only for cell(1,2)
                my_background = QBrush(Qt.red)
                return my_background
        elif role == Qt.TextAlignmentRole:
            if row == 1 and column == 1:                # change text alignment only for cell(1,1)
                return Qt.AlignRight + Qt.AlignVCenter
        elif role == Qt.CheckStateRole:
            if row == 0 and column == 1:                # add checkbox only for cell(0,1)
                return Qt.Checked
            elif row == 0 and column == 2:              # add checkbox only for cell(0,2)
                return Qt.Unchecked

        return QVariant()                               # see http://doc.qt.io/qt-5/qvariant.html#details

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