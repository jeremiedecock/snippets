#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://doc.qt.io/qt-5/qwidget.html#showFullScreen

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

app = QApplication(sys.argv)

# The default constructor has no parent.
# A widget with no parent is a window.
window = QMainWindow()

window.resize(250, 150)
window.setWindowTitle('Hello')

button = QPushButton('Exit', window)
button.clicked.connect(window.close)

window.showFullScreen()                # <- FULLSCREEN

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead. 
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
