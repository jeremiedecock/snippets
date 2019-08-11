#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://hci.isir.upmc.fr/wp-content/uploads/2018/03/PyQt-Dessin.pdf

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QRegion
from PyQt5.QtCore import Qt, QRect
import random


class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.state = False
        self.rect = QRect(5, 5, 150, 150)


    def mousePressEvent(self, event):
        ellipse = QRegion(self.rect, QRegion.Ellipse)

        if ellipse.contains(event.pos()):
            self.state = not self.state

        self.update()                       # call paintEvent()


    def paintEvent(self, event):
        painter = QPainter(self)

        if self.state:
            painter.setBrush(Qt.lightGray)
        else:
            painter.setBrush(Qt.darkCyan)

        painter.drawEllipse(self.rect)


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
