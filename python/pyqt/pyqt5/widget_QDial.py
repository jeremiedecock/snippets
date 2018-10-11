#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://doc.qt.io/qt-5/qslider.html#details

import sys

from PyQt5.QtWidgets import QApplication, QDial


def printValue(value):
    print(value, dial.value())

app = QApplication(sys.argv)

dial = QDial()

#dial.setMinimum(-15)
#dial.setMaximum(15)

dial.setRange(-15, 15)

dial.setNotchesVisible(True)

dial.setValue(5)   # Initial value

dial.valueChanged.connect(printValue)

dial.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
