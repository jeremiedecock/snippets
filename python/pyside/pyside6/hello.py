#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide6 import QtCore, QtWidgets

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())

