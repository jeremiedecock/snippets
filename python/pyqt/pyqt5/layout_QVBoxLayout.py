#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout


app = QApplication(sys.argv)

# Make widgets

window = QWidget()

btn1 = QPushButton("One")
btn2 = QPushButton("Two")
btn3 = QPushButton("Three")

# Set the layout

vbox = QVBoxLayout()

vbox.addWidget(btn1)
vbox.addWidget(btn2)
vbox.addWidget(btn3)

vbox.setContentsMargins(0, 0, 0, 0)  # set the spacing around the layout (in pixels)
vbox.setSpacing(0)                   # set the spacing between elements (in pixels)

window.setLayout(vbox)

# Show
window.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
