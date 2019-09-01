#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://doc.qt.io/qt-5/qpainter.html#drawText

import sys
import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QAction
from PyQt5.QtCore import Qt

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # see https://stackoverflow.com/a/17631703  and  http://doc.qt.io/qt-5/qaction.html#details

        action = QAction(self)
        action.setShortcut(Qt.Key_F)

        action.triggered.connect(self.fullscreen_toggle_key_callback)
        self.addAction(action)


    def fullscreen_toggle_key_callback(self):
        if self.windowState() & Qt.WindowFullScreen:         # https://stackoverflow.com/questions/17834835/test-if-qquickview-qwindow-is-full-screen-in-qt-5-0-x
            self.showNormal()                                # <- NORMAL SCREEN
        else:
            self.showFullScreen()                            # <- FULL SCREEN


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
