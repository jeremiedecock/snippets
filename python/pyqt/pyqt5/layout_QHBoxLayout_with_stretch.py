#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout


app = QApplication(sys.argv)

# Make widgets

window = QWidget()

btn1 = QPushButton("One")
btn2 = QPushButton("Two")
btn3 = QPushButton("Three")

# Set the layout

hbox = QHBoxLayout()

hbox.addStretch(1)    # La méthode addStretch permet d'ajouter un espace de largeur variable, et qui s'ajuste en fonction de la largeur de la fenêtre.
hbox.addWidget(btn1)
hbox.addStretch(1)    # La méthode addStretch permet d'ajouter un espace de largeur variable, et qui s'ajuste en fonction de la largeur de la fenêtre.
hbox.addWidget(btn2)
hbox.addStretch(1)    # La méthode addStretch permet d'ajouter un espace de largeur variable, et qui s'ajuste en fonction de la largeur de la fenêtre.
hbox.addWidget(btn3)
hbox.addStretch(1)    # La méthode addStretch permet d'ajouter un espace de largeur variable, et qui s'ajuste en fonction de la largeur de la fenêtre.

hbox.setContentsMargins(0, 0, 0, 0)  # set the spacing around the layout (in pixels)
hbox.setSpacing(0)                   # set the spacing between elements (in pixels)

window.setLayout(hbox)

# Show
window.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
