#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://www.gchagnon.fr/cours/python/pyqt.html#mep

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QSizePolicy


app = QApplication(sys.argv)

# Make widgets

window = QWidget()

btn1 = QPushButton("One")
btn2 = QPushButton("Two")
btn3 = QPushButton("Three")
btn4 = QPushButton("Four")

# Set the layout

grid = QGridLayout()

grid.addWidget(btn1, 1, 1)   # QWidget, row (int), column (int), rowSpan (int), columnSpan (int), alignment
grid.addWidget(btn2, 2, 2)
grid.addWidget(btn3, 3, 1, 1, 2)
grid.addWidget(btn4, 1, 3, 2, 1)

btn4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # http://doc.qt.io/qt-5/qsizepolicy.html ; https://stackoverflow.com/questions/40580749/why-do-some-widgets-not-stretch-to-fill-the-maximum-space-in-a-layout

grid.setContentsMargins(0, 0, 0, 0)  # set the spacing around the layout (in pixels)
grid.setSpacing(0)                   # set the spacing between elements (in pixels)

window.setLayout(grid)

# Show
window.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
