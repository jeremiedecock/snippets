#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://doc.qt.io/qt-5/qspinbox.html#details

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSpinBox, QPushButton, QVBoxLayout


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Make widgets #################

        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(-15)
        self.spinbox.setMaximum(15)

        self.btn = QPushButton("Print")

        # Set button slot ##############

        self.btn.clicked.connect(self.printText)

        # Set the layout ###############

        vbox = QVBoxLayout()

        vbox.addWidget(self.spinbox)
        vbox.addWidget(self.btn)

        self.setLayout(vbox)

    def printText(self):
        print(self.spinbox.value())


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
