#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://doc.qt.io/qtforpython-6/overviews/qtwidgets-tools-customcompleter-example.html
#     https://doc.qt.io/archives/qt-5.8/qtwidgets-tools-customcompleter-example.html
#     https://code.qt.io/cgit/qt/qtbase.git/tree/examples/widgets/tools/customcompleter?h=5.15

import sys

from PySide6.QtCore import Qt, Slot, QStringListModel
from PySide6.QtGui import QTextCursor, QKeyEvent
from PySide6.QtWidgets import QApplication, QWidget, QPlainTextEdit, QVBoxLayout, QCompleter

class TextEdit(QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setPlaceholderText("Try to type name of planets in our Solar System.")
        self._completer = QCompleter(self)

        self.model = QStringListModel()
        self.model.setStringList(sorted(["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]))  # The list of words to be autocompleted have to be sorted otherwise it won't work!

        self._completer.setModel(self.model)
        self._completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        self._completer.setCaseSensitivity(Qt.CaseInsensitive)
        self._completer.setWrapAround(False)
        self._completer.setWidget(self)
        self._completer.setCompletionMode(QCompleter.PopupCompletion)
        self._completer.activated[str].connect(self.insertCompletion)


    @property
    def completer(self) -> QCompleter:
        return self._completer


    @Slot(str)
    def insertCompletion(self, completion: str):
        tc = self.textCursor()
        extra = len(completion) - len(self._completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)


    def keyPressEvent(self, e: QKeyEvent):
        if self._completer.popup().isVisible():
            if e.key() in [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab]:
                e.ignore()
                return

        super(TextEdit, self).keyPressEvent(e)

        ctrlOrShift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)
        if ctrlOrShift and not e.text():
            return

        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="  # end of word
        hasModifier = e.modifiers() != Qt.NoModifier and not ctrlOrShift

        # Get the text under the cursor
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        completionPrefix = tc.selectedText()

        if hasModifier or not e.text() or len(completionPrefix) < 1 or e.text()[-1] in eow:
            self._completer.popup().hide()
            return

        if completionPrefix != self._completer.completionPrefix():
            self._completer.setCompletionPrefix(completionPrefix)
            self._completer.popup().setCurrentIndex(self._completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self._completer.popup().sizeHintForColumn(0) + self._completer.popup().verticalScrollBar().sizeHint().width())
        self._completer.complete(cr)


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Make widgets #################

        self.edit = TextEdit()

        # Set the layout ###############

        vbox = QVBoxLayout()
        vbox.addWidget(self.edit)
        self.setLayout(vbox)


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
