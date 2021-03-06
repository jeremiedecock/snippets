#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://doc.qt.io/qt-5/qdateedit.html#details

import sys
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QDateEdit, QPushButton, QVBoxLayout


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Make widgets #################

        self.edit1 = QDateEdit()
        self.edit2 = QDateEdit()
        self.edit3 = QDateEdit()

        self.edit1.setMinimumDate(datetime.date(year=2017, month=9, day=1))
        self.edit2.setMinimumDate(datetime.date(year=2017, month=9, day=1))
        self.edit3.setMinimumDate(datetime.date(year=2017, month=9, day=1))

        self.edit1.setMaximumDate(datetime.date(year=2020, month=9, day=1))
        self.edit2.setMaximumDate(datetime.date(year=2020, month=9, day=1))
        self.edit3.setMaximumDate(datetime.date(year=2020, month=9, day=1))

        self.edit1.setDate(datetime.datetime.now().date())
        self.edit2.setDate(datetime.datetime.now().date())
        self.edit3.setDate(datetime.datetime.now().date())

        self.edit1.setCalendarPopup(True)
        self.edit2.setCalendarPopup(True)
        self.edit3.setCalendarPopup(True)

        # Format: see http://doc.qt.io/qt-5/qdatetime.html#toString-2
        self.edit1.setDisplayFormat("yyyy-MM-dd")
        self.edit2.setDisplayFormat("dd/MM/yyyy")
        self.edit3.setDisplayFormat("dddd d MMMM yyyy")

        self.btn = QPushButton("Print")

        # Set button slot ##############

        self.btn.clicked.connect(self.printText)

        # Set the layout ###############

        vbox = QVBoxLayout()

        vbox.addWidget(self.edit1)
        vbox.addWidget(self.edit2)
        vbox.addWidget(self.edit3)

        vbox.addWidget(self.btn)

        self.setLayout(vbox)

    def printText(self):
        print(self.edit1.text())
        print(self.edit2.text())
        print(self.edit3.text())


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
