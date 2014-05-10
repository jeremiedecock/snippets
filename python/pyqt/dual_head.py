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


# See: http://stackoverflow.com/questions/6854947/how-to-display-a-window-on-a-secondary-display-in-pyqt
#      http://pyqt.sourceforge.net/Docs/PyQt4/qdesktopwidget.html#details


import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):
    def __init__(self, name):
        super(Window, self).__init__()

        # Create a label
        label = QtGui.QLabel(name + " (press Esc to quit)")

        # Create the layout
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(label)

        # Set the layout
        self.setLayout(vbox)

        self.resize(250, 150)
        self.setWindowTitle(name)

        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

def main():
    """Main function"""

    app = QtGui.QApplication(sys.argv)

    # For an application, the screen where the main widget resides is the
    # primary screen. This is stored in the primaryScreen property. All windows
    # opened in the context of the application should be constrained to the
    # boundaries of the primary screen; for example, it would be inconvenient
    # if a dialog box popped up on a different screen, or split over two
    # screens.
    desktop = QtGui.QDesktopWidget()

    #print(desktop.numScreens())
    #print(desktop.primaryScreen())

    # The default constructor has no parent.
    # A widget with no parent is a window.
    window0 = Window("Window 0")
    window1 = Window("Window 1")

    qrect0 = desktop.screenGeometry(0)
    qrect1 = desktop.screenGeometry(1)

    window0.move(qrect0.left(), qrect0.top())
    window1.move(qrect1.left(), qrect1.top())

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead. 
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)

if __name__ == '__main__':
    main()


