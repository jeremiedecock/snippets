#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://www.youtube.com/watch?v=U1Nitj0iOgU

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

        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        qp.setRenderHint(QPainter.Antialiasing)           # <- Set anti-aliasing  See https://wiki.python.org/moin/PyQt/Painting%20and%20clipping%20demonstration

        qp.drawEllipse(100, 15, 400, 200)

        qp.translate(100, 100)
        qp.rotate(30)

        qp.setBrush(QBrush(Qt.red, Qt.DiagCrossPattern))

        qp.drawEllipse(600, 15, 200, 100)


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
