#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://hci.isir.upmc.fr/wp-content/uploads/2018/03/PyQt-Dessin.pdf

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import random


class MyWidget(QWidget):

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            btn = "left button"
        elif event.button() == Qt.RightButton:
            btn = "right button"
        elif event.button() == Qt.MidButton:
            btn = "mid button"
        else:
            btn = "unknown button"

        print("press:", event.pos(), btn)

    def mouseReleaseEvent(self, event):
        print("release:", event.pos())

    # Warning: by default mouseMoveEvent sent signal only when mouse buttons are pressed (drag)!
    #          To send mouseMoveEvent even when buttons are not pressed, "mouse tracking" should be activated : self.setMouseTracking(True)
    def mouseMoveEvent(self, event):
        print("move:", event.pos())



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
