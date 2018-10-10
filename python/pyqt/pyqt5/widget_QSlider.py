#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://doc.qt.io/qt-5/qslider.html#details

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QSlider


def printValue(value):
    print(value, slider.value())

app = QApplication(sys.argv)

slider = QSlider(orientation=Qt.Horizontal)
#slider = QSlider(orientation=Qt.Vertical)

slider.setMinimum(-15)
slider.setMaximum(15)

slider.setTickPosition(QSlider.TicksBelow)
slider.setTickInterval(5)

slider.setValue(5)   # Initial value

slider.valueChanged.connect(printValue)

slider.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
