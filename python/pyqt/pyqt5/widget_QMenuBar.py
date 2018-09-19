#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Source: http://www.gchagnon.fr/cours/python/pyqt.html#newapp

import sys
import PyQt5.QtWidgets as widgets

class MainWindow(widgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setUI()

    def setUI(self):

        # Make the Action object
        exitAction = widgets.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip("Quit the application")
        exitAction.triggered.connect(widgets.qApp.exit)

        # Set the menu bar
        menu = self.menuBar()
        fileMenu = menu.addMenu("&File")
        fileMenu.addAction(exitAction)

        # Set the tool bar
        self.toolBar = self.addToolBar('Exit')
        self.toolBar.addAction(exitAction)

        # Set the status bar
        self.statusBar().showMessage('Status bar')

        # Misc
        label = widgets.QLabel("Hello!")
        self.setCentralWidget(label)

        self.show()

if __name__ == '__main__':
    app = widgets.QApplication(sys.argv)
    app.setApplicationName("PyQT Snippets")

    window = MainWindow()

    exit_code = app.exec_()
    sys.exit(exit_code)
