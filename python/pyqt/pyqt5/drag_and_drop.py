#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://pythonspot.com/en/pyqt5-drag-and-drop/

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel


class MyWidget(QWidget):

    def __init__(self):
        super().__init__()

        editBox = QLineEdit('Drag this', self)
        editBox.setDragEnabled(True)
        editBox.move(10, 10)
        editBox.resize(100, 32)

        button = CustomLabel('Drop here.', self)
        button.move(130, 15)

        self.show()


class CustomLabel(QLabel):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
