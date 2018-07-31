#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://pythonspot.com/en/pyqt5-treeview/

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QTreeView, QWidget

class MyTreeWidget(QWidget):
    FROM, SUBJECT, DATE = range(3)

    def __init__(self):
        super().__init__()

        # Create the Tree View
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)

        # Define and set the Model
        model = QStandardItemModel(0, 3, self)
        model.setHeaderData(self.FROM, Qt.Horizontal, "From")
        model.setHeaderData(self.SUBJECT, Qt.Horizontal, "Subject")
        model.setHeaderData(self.DATE, Qt.Horizontal, "Date")

        self.dataView.setModel(model)

        # Add data
        self.addMail(model, 'service@github.com', 'Your Github Donation', '03/25/2017 02:05 PM')
        self.addMail(model, 'support@github.com', 'Github Projects', '02/02/2017 03:05 PM')
        self.addMail(model, 'service@phone.com', 'Your Phone Bill', '01/01/2017 04:05 PM')

        # Set the layout
        layout = QHBoxLayout()
        layout.addWidget(self.dataView)
        self.setLayout(layout)

    def addMail(self, model, mailFrom, subject, date):
        model.insertRow(0)
        model.setData(model.index(0, self.FROM), mailFrom)
        model.setData(model.index(0, self.SUBJECT), subject)
        model.setData(model.index(0, self.DATE), date)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = MyTreeWidget()
    widget.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
