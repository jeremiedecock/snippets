#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://pythonspot.com/en/pyqt5-browser/

##############################################################################
# WARNING: QWebView/QtWebKit are DEPRECATED !!! Use QWebEngineView instead ! #
# (That's why it is not available on Anaconda !)                             #
# See:                                                                       #
# - https://stackoverflow.com/questions/29055475/qwebview-or-qwebengineview  #
# - https://wiki.qt.io/QtWebEngine/Porting_from_QtWebKit                     #
##############################################################################

import sys
from PyQt5.QtCore import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

web = QWebView()
web.load(QUrl("http://www.jdhp.org"))
web.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
