#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Src: https://forum.qt.io/post/415480
# See also: https://doc.qt.io/qt-6/qsharedmemory.html

import sys
from PySide6 import QtCore, QtWidgets

from PySide6.QtCore import QSharedMemory
from PySide6.QtWidgets import QApplication


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    shm = QSharedMemory("62d60669-bb94-4a94-88bb-b964890a7e04")
    if not shm.create(512, QSharedMemory.ReadWrite):
        print("Can't start more than one instance of the application", file=sys.stderr)

        # If SHM is locked by accident (e.g. if previous application instance crashed), it can be unlocked with the following calls:
        # shm.attach()
        # shm.detach()

        sys.exit(1)

    print("Application started successfully")

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
