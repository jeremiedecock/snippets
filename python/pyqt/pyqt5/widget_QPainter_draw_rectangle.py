#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://www.youtube.com/watch?v=0wAU5usATX8/

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt


class MyPaintWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Set window background color
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.white)

        self.setPalette(palette)

    def paintEvent(self, event):
        qp = QPainter(self)

        qp.setRenderHint(QPainter.Antialiasing)           # <- Set anti-aliasing  See https://wiki.python.org/moin/PyQt/Painting%20and%20clipping%20demonstration

        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))

        qp.drawRect(10, 10, 180, 50)   # x_start, y_start, x_length, y_length

        qp.setBrush(QBrush(Qt.red, Qt.DiagCrossPattern))

        qp.drawRect(210, 10, 180, 50)

        qp.setBrush(QBrush(Qt.red, Qt.Dense1Pattern))

        qp.drawRect(410, 10, 180, 50)

        qp.setBrush(QBrush(Qt.red, Qt.HorPattern))

        qp.drawRect(610, 10, 180, 50)

        qp.setBrush(QBrush(Qt.red, Qt.VerPattern))

        qp.drawRect(810, 10, 180, 50)

        qp.setBrush(QBrush(Qt.red, Qt.BDiagPattern))

        qp.drawRect(1010, 10, 180, 50)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = MyPaintWidget()
    widget.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
