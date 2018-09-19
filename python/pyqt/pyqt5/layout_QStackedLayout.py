#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: http://pyqt.sourceforge.net/Docs/PyQt4/qstackedlayout.html


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStackedLayout


app = QApplication(sys.argv)

# Make widgets

window = QWidget()

btn1 = QPushButton("One")
btn2 = QPushButton("Two")
btn3 = QPushButton("Three")

# Set the layout

stack = QStackedLayout()

stack.addWidget(btn1)
stack.addWidget(btn2)
stack.addWidget(btn3)

stack.setCurrentIndex(1)

window.setLayout(stack)

# Show
window.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
