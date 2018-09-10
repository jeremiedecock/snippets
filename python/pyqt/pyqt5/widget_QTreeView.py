#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://pythonspot.com/en/pyqt5-treeview/

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QTreeView


class MyModel(QStandardItemModel):
    FROM, SUBJECT, DATE = range(3)

    def __init__(self):
        super().__init__(0, 3, None)

        # Define and set the Model
        self.setHeaderData(self.FROM, Qt.Horizontal, "From")
        self.setHeaderData(self.SUBJECT, Qt.Horizontal, "Subject")
        self.setHeaderData(self.DATE, Qt.Horizontal, "Date")

    def addMail(self, mail_from, subject, date):
        self.insertRow(0)
        self.setData(self.index(0, self.FROM), mail_from)
        self.setData(self.index(0, self.SUBJECT), subject)
        self.setData(self.index(0, self.DATE), date)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dataView = QTreeView()
    dataView.setRootIsDecorated(False)
    dataView.setAlternatingRowColors(True)

    model = MyModel()

    # Add data
    model.addMail('service@github.com', 'Your Github Donation', '03/25/2017 02:05 PM')
    model.addMail('support@github.com', 'Github Projects', '02/02/2017 03:05 PM')
    model.addMail('service@phone.com', 'Your Phone Bill', '01/01/2017 04:05 PM')

    dataView.setModel(model)
    dataView.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
