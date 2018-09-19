#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://www.youtube.com/watch?v=96FBrNR3XOY

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QPolygon
from PyQt5.QtCore import Qt, QPoint


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
        #qp.setBrush(QBrush(Qt.red, Qt.DiagCrossPattern))

        points = QPolygon([
            QPoint(10, 10),
            QPoint(20, 100),
            QPoint(100, 50),
            QPoint(150, 10),
            QPoint(100, 100)
        ])

        qp.drawPolygon(points)


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
