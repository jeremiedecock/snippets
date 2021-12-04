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
        print()
        print("proposed actions:", event.proposedAction())
        print("text:", event.mimeData().text())
        print("data:")

        for format_str in event.mimeData().formats():
            data = event.mimeData().data(format_str)
            print("- {}: {}".format(format_str, data))

        event.acceptProposedAction()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Windows()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())

