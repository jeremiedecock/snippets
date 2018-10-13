#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://doc.qt.io/qt-5/qcombobox.html#details

import sys
from PyQt5.QtWidgets import QApplication, QComboBox


def printText(index):
    print(combobox.currentText())

app = QApplication(sys.argv)

combobox = QComboBox()
combobox.addItems(["Linux", "MacOS", "Windows"])
#combobox.setCurrentIndex(1)
combobox.setCurrentText("MacOS")
combobox.currentIndexChanged.connect(printText)

combobox.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
