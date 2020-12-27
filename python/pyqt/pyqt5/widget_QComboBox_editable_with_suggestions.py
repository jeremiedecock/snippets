#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://stackoverflow.com/questions/22125933/how-to-create-autocomplete-combobox-in-pyqt4
#     https://doc.qt.io/qtforpython/PySide6/QtWidgets/QComboBox.html?highlight=completer#PySide6.QtWidgets.PySide6.QtWidgets.QComboBox.completer
#     https://doc.qt.io/qtforpython/overviews/qtwidgets-tools-completer-example.html?highlight=completer

import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QCompleter


def printText(index):
    print(combobox.currentText())

app = QApplication(sys.argv)

combobox = QComboBox()

#"Select one...",
ITEMS = ["",
         "ActionScript",
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
                                                                                                                                                                                            
combobox.addItems(ITEMS)
combobox.setEditable(True)
combobox.completer().setCompletionMode(QCompleter.PopupCompletion)
#combobox.setCurrentIndex(1)
#combobox.setCurrentText("Python")
combobox.currentIndexChanged.connect(printText)

combobox.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
