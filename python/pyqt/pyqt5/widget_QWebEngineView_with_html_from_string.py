#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://doc.qt.io/qt-5/qwebengineview.html#details

# This class replace the deprecated QWebView (based on QtWebKit).
# See:
# - https://stackoverflow.com/questions/29055475/qwebview-or-qwebengineview
# - https://wiki.qt.io/QtWebEngine/Porting_from_QtWebKit

HTML = r'''<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <style type="text/css" media="all">
* {
    border-width      : 0px;

    font-family       : monospace,fixed;
    font-size         : 32px;

    margin            : 0px;
    padding           : 0px;
}

p {
    background-color  : #ee0000;
}
        </style>
    </head>
    <body>

        <p>Hello!</p>

    </body>
</html>
'''

# The next two lines are a workaround to fix an issue with QWebEngineView (see https://github.com/ContinuumIO/anaconda-issues/issues/9199#issuecomment-383842265)
import ctypes
ctypes.CDLL("libGL.so.1", mode=ctypes.RTLD_GLOBAL)

import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

web = QWebEngineView()
web.setHtml(HTML)
web.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
