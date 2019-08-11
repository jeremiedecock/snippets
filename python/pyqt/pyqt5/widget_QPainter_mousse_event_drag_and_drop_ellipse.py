#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://hci.isir.upmc.fr/wp-content/uploads/2018/03/PyQt-Dessin.pdf

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QRegion
from PyQt5.QtCore import Qt, QRect
import random

SIZE = 30

class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.rect = QRect(5, 5, SIZE, SIZE)
        self.relative_pos = None
        self.grabbed = False


    def mousePressEvent(self, event):
        ellipse = QRegion(self.rect, QRegion.Ellipse)

        if ellipse.contains(event.pos()):
            self.grabbed = True
            self.relative_pos = (event.pos().x() - self.rect.left(), event.pos().y() - self.rect.top())


    def mouseReleaseEvent(self, event):
        self.grabbed = False


    # Warning: by default mouseMoveEvent sent signal only when mouse buttons are pressed (drag)!
    #          To send mouseMoveEvent even when buttons are not pressed, "mouse tracking" should be activated : self.setMouseTracking(True)
    def mouseMoveEvent(self, event):
        if self.grabbed:
            self.rect = QRect(event.pos().x() - self.relative_pos[0], event.pos().y() - self.relative_pos[1], SIZE, SIZE)
            self.update()                  # call paintEvent()


    def paintEvent(self, event):
        painter = QPainter(self)
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
