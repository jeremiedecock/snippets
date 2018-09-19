#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout


app = QApplication(sys.argv)

# Make the window

window = QWidget()

# Make widgets

btn1 = QPushButton("One")
widget = QWidget()

btn2 = QPushButton("Two")
btn3 = QPushButton("Three")

# VBox

vbox = QVBoxLayout()

vbox.addWidget(btn1)
vbox.addWidget(widget)

# HBox

hbox = QHBoxLayout()

hbox.addWidget(btn2)
hbox.addWidget(btn3)

# Set layouts

window.setLayout(vbox)
widget.setLayout(hbox)

# Show

window.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
