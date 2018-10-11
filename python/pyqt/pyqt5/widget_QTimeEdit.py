#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://doc.qt.io/qt-5/qtimeedit.html#details

import sys
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QTimeEdit, QPushButton, QVBoxLayout


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Make widgets #################

        self.edit1 = QTimeEdit()
        self.edit2 = QTimeEdit()
        self.edit3 = QTimeEdit()

        self.edit1.setMinimumTime(datetime.time(hour=8, minute=30, second=30))
        self.edit2.setMinimumTime(datetime.time(hour=8, minute=30, second=30))
        self.edit3.setMinimumTime(datetime.time(hour=8, minute=30, second=30))

        self.edit1.setMaximumTime(datetime.time(hour=18, minute=30, second=30))
        self.edit2.setMaximumTime(datetime.time(hour=18, minute=30, second=30))
        self.edit3.setMaximumTime(datetime.time(hour=18, minute=30, second=30))

        self.edit1.setTime(datetime.datetime.now().time())
        self.edit2.setTime(datetime.datetime.now().time())
        self.edit3.setTime(datetime.datetime.now().time())

        # Format: see http://doc.qt.io/qt-5/qdatetime.html#toString-2
        self.edit1.setDisplayFormat("HH:mm")
        self.edit2.setDisplayFormat("HH:mm:ss t")
        self.edit3.setDisplayFormat("h m AP")

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
