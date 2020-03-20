#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://doc.qt.io/qt-5/qpainter.html#drawText

import sys
import datetime

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QTimer

def getTime():
    t = datetime.datetime.now().strftime("%H:%M:%S")
    return t

class MyPaintWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Set window background color
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.white)

        self.setPalette(palette)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # ms

    def paintEvent(self, event):
        qp = QPainter(self)

        font = qp.font()
        font.setPointSize(32)
        qp.setFont(font)

        size = self.size()
        qp.drawText(0, 0, size.width(), size.height(), Qt.AlignCenter, getTime())


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
