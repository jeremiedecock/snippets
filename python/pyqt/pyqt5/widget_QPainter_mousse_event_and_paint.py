#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://hci.isir.upmc.fr/wp-content/uploads/2018/03/PyQt-Dessin.pdf

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import random


class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.cursor_pos = None

    # Warning: by default mouseMoveEvent sent signal only when mouse buttons are pressed (drag)!
    #          To send mouseMoveEvent even when buttons are not pressed, "mouse tracking" should be activated : self.setMouseTracking(True)
    def mouseMoveEvent(self, event):
        self.cursor_pos = event.pos()
        self.update()                  # call paintEvent()

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.cursor_pos is not None:
            painter.drawEllipse(self.cursor_pos.x()-7, self.cursor_pos.y()-7, 10, 10)


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
