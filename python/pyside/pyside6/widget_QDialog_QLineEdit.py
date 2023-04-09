#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://www.pythonguis.com/tutorials/pyqt-dialogs/

import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLineEdit, QVBoxLayout, QLabel, QDialogButtonBox


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("HELLO!")

        # print(self.width(), self.height())
        self.resize(600, self.height())

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Make widgets #################

        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Type something here and press the 'Print' button")

        # Set the layout ###############

        vbox = QVBoxLayout()

        vbox.addWidget(self.edit)
        vbox.addWidget(self.button_box)

        self.setLayout(vbox)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        button = QPushButton('Clic me', self)
        button.clicked.connect(self.on_clic)

    def on_clic(self):
        dialog = CustomDialog(parent=self)
        if dialog.exec():
            print("Success!")
            print(dialog.edit.text())
        else:
            print("Cancel!")


app = QApplication(sys.argv)

window = Window()
window.show()

exit_code = app.exec_()
sys.exit(exit_code)
