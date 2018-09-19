#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QBoxLayout


app = QApplication(sys.argv)

# Make widgets

window = QWidget()

btn1 = QPushButton("One")
btn2 = QPushButton("Two")
btn3 = QPushButton("Three")

# Set the layout

box = QBoxLayout(QBoxLayout.Direction(0))  # TODO

box.addWidget(btn1)
box.addWidget(btn2)
box.addWidget(btn3)

box.setContentsMargins(0, 0, 0, 0)  # set the spacing around the layout (in pixels)
box.setSpacing(0)                   # set the spacing between elements (in pixels)

window.setLayout(box)

# Show
window.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
