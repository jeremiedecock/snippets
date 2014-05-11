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


# TODO
# - size of pixmaps
# - add a clock on the note screen (and update it every seconds) -> cf. QTimer
# - check command options
# - fix the bug zoom in then zoom out (vertically recenter the label)
# - gérer le cas avec 1 seul écran
# - gérer le cas avec 3 écrans et plus -> permettre de spécifier les numéros d'écrans à utiliser dans les options


import sys
import argparse

from PyQt4 import QtGui, QtCore

import popplerqt4

class Screen():
    def __init__(self, num, geometry, size):
        self.num = num
        self.geometry = geometry
        self.size = size


class PDFController():
    # TODO
    def __init__(self, window_slides, window_notes, screen_0, screen_1):
        self.window_slides = window_slides
        self.window_notes = window_notes
        self.screens = (screen_0, screen_1)

        self.current_page_num = -1
        self.num_pages = max(self.window_slides.num_pages, self.window_notes.num_pages)

    def update(self, e):
        # See http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#Key-enum for all keys
        if e.key() == QtCore.Qt.Key_Escape:
            self.window_slides.close()
            self.window_notes.close()

        elif e.key() == QtCore.Qt.Key_Return:
            self.current_page_num = min(self.current_page_num + 1, self.num_pages - 1)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Space:
            self.current_page_num = min(self.current_page_num + 1, self.num_pages - 1)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_PageUp:
            self.current_page_num = min(self.current_page_num + 5, self.num_pages - 1)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_PageDown:
            self.current_page_num = max(self.current_page_num - 5, 0)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Home:
            self.current_page_num = 0
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_End:
            self.current_page_num = self.num_pages - 1
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Left:
            self.current_page_num = max(self.current_page_num - 1, 0)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Right:
            self.current_page_num = min(self.current_page_num + 1, self.num_pages - 1)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Up:
            self.current_page_num = min(self.current_page_num + 1, self.num_pages - 1)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Down:
            self.current_page_num = max(self.current_page_num - 1, 0)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Plus:
            self.window_slides.scale_factor += 0.1
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Minus:
            self.window_slides.scale_factor -= 0.1
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Tab:
            # Switch screen
            self.screens = (self.screens[1], self.screens[0])

            self.window_slides.showNormal() # required
            self.window_notes.showNormal()  # required

            self.window_slides.move(self.screens[0].geometry.left(), self.screens[0].geometry.top())
            self.window_notes.move(self.screens[1].geometry.left(), self.screens[1].geometry.top())

            self.window_slides.showFullScreen()
            self.window_notes.showFullScreen()

            self.renderCurrentPage()

    def renderCurrentPage(self):
        self.window_slides.updatePdfPagePixmap()
        self.window_notes.updatePdfPagePixmap()



class Window(QtGui.QWidget):
    def __init__(self, name, doc, screen):
        super(Window, self).__init__()

        self.name = name
        self.pdf_controller = None
        self.scale_factor = 1.0

        self.doc = doc
        self.screen = screen

        self.num_pages = self.doc.numPages()

        # Create a label with the pixmap
        self.label = QtGui.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)  # To center the label (ie the image)

        # Create the layout
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.label)

        # Set the layout
        self.setLayout(vbox)

        self.resize(800, 600)
        self.setWindowTitle(name)
        self.setStyleSheet("background-color:black;")  # TODO: or white ?

        #self.show()

    def updatePdfPagePixmap(self):
        if self.pdf_controller is not None:
            page = self.doc.page(self.pdf_controller.current_page_num)

            if page is not None:
                print self.name, "---"
                print self.frameSize().width()
                print self.frameSize().height()
                print page.pageSize().width()
                print page.pageSize().height()
                print "---"

                #ratio_x = self.scale_factor * self.frameSize().width() / page.pageSize().width()
                #ratio_y = self.scale_factor * self.frameSize().height() / page.pageSize().height()
                ratio_x = self.scale_factor * self.screen.size.width() / page.pageSize().width()
                ratio_y = self.scale_factor * self.screen.size.height() / page.pageSize().height()
                #ratio_x = self.scale_factor * 1920 / page.pageSize().width()
                #ratio_y = self.scale_factor * 1080 / page.pageSize().height()
                ratio = min(ratio_x, ratio_y)

                # See http://people.freedesktop.org/~aacid/docs/qt4/classPoppler_1_1Page.html
                # page.renderToImage(xres=72.0, yres=72.0, x=-1, y=-1, width=-1, height=-1, rotate)
                # 
                # Parameters
                #   x   specifies the left x-coordinate of the box, in pixels.
                #   y   specifies the top y-coordinate of the box, in pixels.
                #   w   specifies the width of the box, in pixels.
                #   h   specifies the height of the box, in pixels.
                #   xres    horizontal resolution of the graphics device, in dots per inch
                #   yres    vertical resolution of the graphics device, in dots per inch
                #   rotate  how to rotate the page
                image = page.renderToImage(72. * ratio, 72. * ratio)
                pixmap = QtGui.QPixmap.fromImage(image)

                self.label.setPixmap(pixmap)
                #self.label.resize(self.label.sizeHint())
            else:
                self.label.setPixmap(None)

    def keyPressEvent(self, e):
        if self.pdf_controller is not None:
            self.pdf_controller.update(e)

def main():
    """Main function"""

    # PARSE OPTIONS ###################

    parser = argparse.ArgumentParser(description='PDF Presenter Dual Head.')

    parser.add_argument("--notes", "-n",  help="Notes (PDF files)", metavar="FILE")
    parser.add_argument("fileargs", nargs=1, metavar="FILE", help="Slides (PDF file)")

    args = parser.parse_args()

    # TODO: test arguments

    # POPPLER #########################

    slides_doc = popplerqt4.Poppler.Document.load(args.fileargs[0])
    #slides_doc.setRenderBackend(popplerqt4.Poppler.Document.SplashBackend) # ok (default)
    #slides_doc.setRenderBackend(popplerqt4.Poppler.Document.ArthurBackend) # bad
    slides_doc.setRenderHint(popplerqt4.Poppler.Document.Antialiasing)
    slides_doc.setRenderHint(popplerqt4.Poppler.Document.TextAntialiasing)

    notes_doc = popplerqt4.Poppler.Document.load(args.notes)
    #notes_doc.setRenderBackend(popplerqt4.Poppler.Document.SplashBackend) # ok (default)
    #notes_doc.setRenderBackend(popplerqt4.Poppler.Document.ArthurBackend) # bad
    notes_doc.setRenderHint(popplerqt4.Poppler.Document.Antialiasing)
    notes_doc.setRenderHint(popplerqt4.Poppler.Document.TextAntialiasing)

    # QT4 #############################

    app = QtGui.QApplication(sys.argv)

    # For an application, the screen where the main widget resides is the
    # primary screen. This is stored in the primaryScreen property. All windows
    # opened in the context of the application should be constrained to the
    # boundaries of the primary screen; for example, it would be inconvenient
    # if a dialog box popped up on a different screen, or split over two
    # screens.
    desktop = QtGui.QDesktopWidget()

    screen0 = Screen(0, desktop.screenGeometry(0), desktop.screen(0).frameSize())
    screen1 = Screen(1, desktop.screenGeometry(1), desktop.screen(1).frameSize())

    # The default constructor has no parent.
    # A widget with no parent is a window.
    window_slides = Window("PDF Presenter (Slides)", slides_doc, screen0)
    window_notes = Window("PDF Presenter (Notes)", notes_doc, screen1)

    window_slides.move(screen0.geometry.left(), screen0.geometry.top())
    window_notes.move(screen1.geometry.left(), screen1.geometry.top())

    window_slides.showFullScreen()
    window_notes.showFullScreen()

    pdf_controller = PDFController(window_slides, window_notes, screen0, screen1)
    window_slides.pdf_controller = pdf_controller
    window_notes.pdf_controller = pdf_controller

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead. 
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)

if __name__ == '__main__':
    main()


