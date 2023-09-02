#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://doc.qt.io/qtforpython-6/overviews/qtwidgets-tools-customcompleter-example.html
#     https://doc.qt.io/archives/qt-5.8/qtwidgets-tools-customcompleter-example.html
#     https://code.qt.io/cgit/qt/qtbase.git/tree/examples/widgets/tools/customcompleter?h=5.15

import sys

from PySide6.QtCore import Qt, Slot, QStringListModel
from PySide6.QtGui import QTextCursor, QKeyEvent, QFocusEvent
from PySide6.QtWidgets import QApplication, QWidget, QPlainTextEdit, QVBoxLayout, QCompleter

class TextEdit(QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setPlainText("This TextEdit provides autocompletions for words that have more than"
                          " 3 characters. You can trigger autocompletion using Ctrl+E")
        self.c = None

    def setCompleter(self, completer: QCompleter):
        if self.c:
            self.c.disconnect(self)

        self.c = completer

        if not self.c:
            return

        self.c.setWidget(self)
        self.c.setCompletionMode(QCompleter.PopupCompletion)
        self.c.setCaseSensitivity(Qt.CaseInsensitive)
        self.c.activated[str].connect(self.insertCompletion)

    @property
    def completer(self) -> QCompleter:
        return self.c

    @Slot(str)
    def insertCompletion(self, completion: str):
        if self.c.widget() != self:
            return
        tc = self.textCursor()
        extra = len(completion) - len(self.c.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def textUnderCursor(self) -> str:
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, e: QFocusEvent):
        if self.c:
            self.c.setWidget(self)
        super(TextEdit, self).focusInEvent(e)

    def keyPressEvent(self, e: QKeyEvent):
        if self.c and self.c.popup().isVisible():
            if e.key() in [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab]:
                e.ignore()
                return

        isShortcut = e.modifiers() & Qt.ControlModifier and e.key() == Qt.Key_E
        if not self.c or not isShortcut:
            super(TextEdit, self).keyPressEvent(e)

        ctrlOrShift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)
        if not self.c or (ctrlOrShift and not e.text()):
            return

        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="  # end of word
        hasModifier = e.modifiers() != Qt.NoModifier and not ctrlOrShift
        completionPrefix = self.textUnderCursor()

        if (not isShortcut and (hasModifier or not e.text() or len(completionPrefix) < 3
                                or e.text()[-1] in eow)):
            self.c.popup().hide()
            return

        if completionPrefix != self.c.completionPrefix():
            self.c.setCompletionPrefix(completionPrefix)
            self.c.popup().setCurrentIndex(self.c.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self.c.popup().sizeHintForColumn(0) + self.c.popup().verticalScrollBar().sizeHint().width())
        self.c.complete(cr)


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Make widgets #################

        self.edit = TextEdit()

        self.completer = QCompleter(self)

        self.model = QStringListModel()
        self.model.setStringList(["aaaaa", "bbbbbb", "cccccc", "dddddd"])

        self.completer.setModel(self.model)
        self.completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setWrapAround(False)

        self.edit.setCompleter(self.completer)

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
