#!/usr/bin/env python
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

# Debian packages required:
# - python-poppler-qt4  (not python-poppler)

# See: http://stackoverflow.com/questions/10562945/how-to-display-pdf-with-python-poppler-qt4
#      http://web.archive.org/web/20120417095851/http://www.rkblog.rk.edu.pl/w/p/rendering-pdf-files-pyqt4-pypoppler-qt4/
#      http://bazaar.launchpad.net/~j-corwin/openlp/pdf/annotate/head:/openlp/plugins/presentations/lib/pdfcontroller.py


import sys
from PyQt4 import QtGui, QtCore

import popplerqt4

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        # Poppler (PDF render)
        doc = popplerqt4.Poppler.Document.load("test.pdf")
        #doc.setRenderBackend(popplerqt4.Poppler.Document.SplashBackend) # ok (default)
        #doc.setRenderBackend(popplerqt4.Poppler.Document.ArthurBackend) # bad
        doc.setRenderHint(popplerqt4.Poppler.Document.Antialiasing)
        doc.setRenderHint(popplerqt4.Poppler.Document.TextAntialiasing)

        page = doc.page(0)

        # See http://people.freedesktop.org/~aacid/docs/qt4/classPoppler_1_1Page.html
        # page.renderToImage(xres=72.0, yres=72.0, x=-1, y=-1, width=-1, height=-1, rotate)
        # 
        # Parameters
        #   xres    horizontal resolution of the graphics device, in dots per inch
        #   yres    vertical resolution of the graphics device, in dots per inch
        #   x   specifies the left x-coordinate of the box, in pixels.
        #   y   specifies the top y-coordinate of the box, in pixels.
        #   w   specifies the width of the box, in pixels.
        #   h   specifies the height of the box, in pixels.
        #   rotate  how to rotate the page
        #image = page.renderToImage(300.0, 300.0, -1, -1, -1, -1)
        image = page.renderToImage()
        pixmap = QtGui.QPixmap.fromImage(image)

        # Create a label with the pixmap
        label = QtGui.QLabel(self)
        label.setPixmap(pixmap)

        # Create the layout
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(label)

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


