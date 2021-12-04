#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://doc.qt.io/qtforpython/overviews/dnd.html

import sys
from PySide6 import QtCore, QtWidgets

class Windows(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)

        self.text = QtWidgets.QLabel("Drop content here...", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)


    def dragEnterEvent(self, event):
        #if (event.mimeData().hasFormat("text/plain"))
        event.acceptProposedAction()


    def dropEvent(self, event):
        url_bytes = event.mimeData().data("text/x-moz-text-internal")
        url_str = url_bytes.data().decode("utf-16")
        print(url_str)

        event.acceptProposedAction()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Windows()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())

