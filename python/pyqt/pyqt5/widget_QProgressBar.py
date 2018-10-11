#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://doc.qt.io/qt-5/qprogressbar.html#details

import sys

from PyQt5.QtWidgets import QApplication, QProgressBar, QWidget, QVBoxLayout


app = QApplication(sys.argv)

window = QWidget()

progressbar_1 = QProgressBar()
progressbar_1.setRange(0, 100)
progressbar_1.setValue(70)

progressbar_2 = QProgressBar()
progressbar_2.setRange(0, 0)

vbox = QVBoxLayout()
vbox.addWidget(progressbar_1)
vbox.addWidget(progressbar_2)

window.setLayout(vbox)

window.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
