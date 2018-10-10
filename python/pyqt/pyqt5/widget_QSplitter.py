#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://doc.qt.io/qt-5/qsplitter.html#details

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QSplitter, QTextEdit

app = QApplication(sys.argv)

#splitter = QSplitter(orientation=Qt.Horizontal)
splitter = QSplitter(orientation=Qt.Vertical)

widget1 = QTextEdit()
widget2 = QTextEdit()
widget3 = QTextEdit()

splitter.addWidget(widget1)
splitter.addWidget(widget2)
splitter.addWidget(widget3)

splitter.resize(400, 400)

splitter.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
