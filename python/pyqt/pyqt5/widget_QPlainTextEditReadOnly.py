#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://doc.qt.io/qt-5/qtextedit.html#details

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit, QVBoxLayout

text = """Maître Corbeau, sur un arbre perché,
Tenait en son bec un fromage.
Maître Renard, par l’odeur alléché,
Lui tint à peu près ce langage :
Eh ! bonjour, Monsieur du Corbeau.
Que vous êtes joli ! que vous me semblez beau !
Sans mentir, si votre ramage
Se rapporte à votre plumage,
Vous êtes le Phénix des hôtes de ces bois.
À ces mots le Corbeau ne se sent pas de joie ;
Et pour montrer sa belle voix,
Il ouvre un large bec, laisse tomber sa proie.
Le Renard s’en saisit, et dit : Mon bon Monsieur,
Apprenez que tout flatteur
Vit aux dépens de celui qui l’écoute.
Cette leçon vaut bien un fromage, sans doute.
Le Corbeau, honteux et confus,
Jura, mais un peu tard, qu’on ne l’y prendrait plus."""

class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Make widgets #################

        self.edit = QPlainTextEdit()

        self.edit.setPlainText(text)

        self.edit.setReadOnly(True)

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
