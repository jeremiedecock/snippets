#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://stackoverflow.com/questions/22125933/how-to-create-autocomplete-combobox-in-pyqt4
#     https://doc.qt.io/qt-5/qcompleter.html
#     https://doc.qt.io/qtforpython/PySide6/QtWidgets/QLineEdit.html?highlight=completer#PySide6.QtWidgets.PySide6.QtWidgets.QLineEdit.completer
#     https://doc.qt.io/qtforpython/overviews/qtwidgets-tools-completer-example.html?highlight=completer

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QCompleter


ITEMS = ["ActionScript",
         "AppleScript",
         "Asp",
         "BASIC",
         "C",
         "C++",
         "Clojure",
         "COBOL",
         "ColdFusion",
         "Erlang",
         "Fortran",
         "Groovy",
         "Haskell",
         "Java",
         "JavaScript",
         "Lisp",
         "Perl",
         "PHP",
         "Python",
         "Ruby",
         "Scala",
         "Scheme"]

class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Make widgets #################

        self.edit = QLineEdit()
        self.btn = QPushButton("Print")

        self.edit.setPlaceholderText("Type something here and press the 'Print' button")

        # Set completer ################

        completer = QCompleter(ITEMS)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.edit.setCompleter(completer)

        # Set button slot ##############

        self.btn.clicked.connect(self.printText)

        # Set the layout ###############

        vbox = QVBoxLayout()

        vbox.addWidget(self.edit)
        vbox.addWidget(self.btn)

        self.setLayout(vbox)

    def printText(self):
        print(self.edit.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
