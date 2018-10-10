#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://doc.qt.io/qt-5/qpushbutton.html#details

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        button = QPushButton('Hello', self)
        button.clicked.connect(self.on_clic)

    def on_clic(self):
        print("Hello!")


app = QApplication(sys.argv)

window = Window()
window.show()

exit_code = app.exec_()
sys.exit(exit_code)
