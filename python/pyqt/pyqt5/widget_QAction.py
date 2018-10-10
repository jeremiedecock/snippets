#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QSizePolicy

app = QApplication(sys.argv)

# The default constructor has no parent.
# A widget with no parent is a window.
window = QMainWindow()

window.setWindowTitle('Hello')

label = QLabel("Press Ctrl+P to print a message on the terminal", window)
label.resize(800, 100)

# Set key shortcut ################################

def action_callback():
    print("Hello!")


# see https://stackoverflow.com/a/17631703  and  http://doc.qt.io/qt-5/qaction.html#details

action = QAction(label)                    # <-
action.setShortcut(Qt.Key_P | Qt.CTRL)     # <-

action.triggered.connect(action_callback)  # <-
label.addAction(action)                    # <-

###################################################

window.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead. 
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
