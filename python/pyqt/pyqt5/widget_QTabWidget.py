#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://pythonspot.com/en/pyqt5-tabs/

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, QVBoxLayout


class MyTabWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)

        tab1 = QWidget()
        tab2 = QWidget()

        # Add tabs
        self.tabs.addTab(tab1, "Tab 1")
        self.tabs.addTab(tab2, "Tab 2")

        # Populate the first tab
        button1 = QPushButton("PyQt5 button")
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(button1)
        tab1.setLayout(tab1_layout)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = MyTabWidget()
    widget.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
