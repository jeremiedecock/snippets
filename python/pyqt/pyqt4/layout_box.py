#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Jérémie DECOCK (http://www.jdhp.org)

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


# See: http://web.archive.org/web/20120501112552/http://zetcode.com/tutorials/pyqt4/layoutmanagement
#      http://pyqt.sourceforge.net/Docs/PyQt4/qboxlayout.html


import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        # Create push buttons
        btn1 = QtGui.QPushButton('Btn1')
        btn2 = QtGui.QPushButton('Btn2')

        # Create the layouts
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)

        # Set the layout
        self.setLayout(vbox)

        self.resize(250, 150)
        self.setWindowTitle('Hello')
        self.show()

def main():
    """Main function"""

    app = QtGui.QApplication(sys.argv)

    # The default constructor has no parent.
    # A widget with no parent is a window.
    window = Window()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead. 
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)

if __name__ == '__main__':
    main()


