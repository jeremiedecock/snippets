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


# See: http://web.archive.org/web/20120401070521/http://zetcode.com/tutorials/pyqt4/eventsandsignals/


import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        # Create a push button.
        self.label = QtGui.QLabel('Press any key (Esc to quit)')

        # Create the layout
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.label)

        # Set the layout
        self.setLayout(vbox)

        self.resize(250, 150)
        self.setWindowTitle('Hello')
        self.show()

    def keyPressEvent(self, e):
        # See http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#Key-enum for all keys
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

        elif e.key() == QtCore.Qt.Key_Return:
            self.label.setText("Return")

        elif e.key() == QtCore.Qt.Key_Space:
            self.label.setText("Space")

        elif e.key() == QtCore.Qt.Key_PageUp:
            self.label.setText("PageUp")

        elif e.key() == QtCore.Qt.Key_PageDown:
            self.label.setText("PageDown")

        elif e.key() == QtCore.Qt.Key_Shift:
            self.label.setText("Shift")

        elif e.key() == QtCore.Qt.Key_Control:
            self.label.setText("Control")

        elif e.key() == QtCore.Qt.Key_Alt:
            self.label.setText("Alt")

        elif e.key() == QtCore.Qt.Key_AltGr:
            self.label.setText("AltGr")

        elif e.key() == QtCore.Qt.Key_Tab:
            self.label.setText("Tab")

        elif e.key() == QtCore.Qt.Key_Home:
            self.label.setText("Home")

        elif e.key() == QtCore.Qt.Key_End:
            self.label.setText("End")

        elif e.key() == QtCore.Qt.Key_Delete:
            self.label.setText("Delete")

        elif e.key() == QtCore.Qt.Key_Left:
            self.label.setText("Left")

        elif e.key() == QtCore.Qt.Key_Right:
            self.label.setText("Right")

        elif e.key() == QtCore.Qt.Key_Up:
            self.label.setText("Up")

        elif e.key() == QtCore.Qt.Key_Down:
            self.label.setText("Down")

        else:
            self.label.setText(str(e.key()))

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


