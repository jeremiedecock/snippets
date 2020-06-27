#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref:
# - http://doc.qt.io/qt-5/modelview.html#3-4-delegates
# - http://doc.qt.io/qt-5/model-view-programming.html#delegate-classes
# - http://doc.qt.io/qt-5/qabstractitemdelegate.html#details
# - http://doc.qt.io/qt-5/qitemdelegate.html#details
# - http://doc.qt.io/qt-5/qstyleditemdelegate.html#details
# - http://doc.qt.io/qt-5/qtwidgets-itemviews-spinboxdelegate-example.html

import sys
import datetime

from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtWidgets import QApplication, QTableView, QStyledItemDelegate, QSpinBox

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DATA = [
    'cent',
    'deux cents',
    'trois cents',
]

###############################################################################

class MyModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = [0, 0, 0]        # DON'T CALL THIS ATTRIBUTE "data", A METHOD ALREADY HAVE THIS NAME (model.data(index, role)) !!!

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            # See https://stackoverflow.com/a/8480223
            return self._data[index.row()]
        return QVariant()

    def setData(self, index, value, role):
        if role == Qt.EditRole:

            try:
                self._data[index.row()] = value

                # The following line are necessary e.g. to dynamically update the QSortFilterProxyModel
                self.dataChanged.emit(index, index, [Qt.EditRole])
            except Exception as e:
                print(e)
                return False

        return True

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

###############################################################################

# https://doc.qt.io/qt-5/model-view-programming.html#delegates
# https://doc.qt.io/qt-5/model-view-programming.html#delegate-classes
# https://doc.qt.io/qt-5/qabstractitemdelegate.html
# https://doc.qt.io/qt-5/qitemdelegate.html
# https://doc.qt.io/qt-5/qstyleditemdelegate.html
class MyDelegate(QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        """
        Crée le widget utilisé pour éditer la valeur d'une cellule
        
        Retourne un widget "vierge", i.e. ce n'est pas ici qu'on initialise la valeur du widget.
        En revanche, c'est ici qu'on peut définir les valeurs min/max acceptées, etc.

        https://doc.qt.io/qt-5/model-view-programming.html#providing-an-editor
        """
        editor = QSpinBox(parent=parent)
        editor.setMinimum(0)
        editor.setMaximum(len(DATA) - 1)   # TODO

        # setFrame(): tell whether the line edit draws itself with a frame.
        # If enabled (the default) the line edit draws itself inside a frame, otherwise the line edit draws itself without any frame.
        editor.setFrame(False)

        return editor


    def setEditorData(self, editor, index):
        """
        Initialise la valeur du widget utilisé pour éditer la valeur d'une cellule.
        La donnée du modèle peut être récupérée via l'argument "index" (index.data(), index.model(), ...).

        Cette méthode:
        1. récupère la donnée du **modèle** (index.data(), ...)
        2. appèle la méthode approprée pour initialiser le widget editor (e.g. editor.setValue(value) si c'est un QSpinBox, ...)

        Mémo: model.data() -> editor.setValue()
        """
        value = int(index.data(Qt.EditRole))       # equivalent of    value = index.model().data(index, Qt.EditRole)      # <<< TODO: display role or editor role ?
        editor.setValue(value)


    def setModelData(self, editor, model, index):
        """
        Submit editor's (widget) data to the *model*
        When the user has finished editing the value in the spin box, the view asks the delegate to store the edited value in the model by calling the setModelData() function.

        Cette méthode:
        1. récupère la donnée du **widget editor** avec la méthode appropriée (e.g. editor.value() si editor est un QSpinBox...)
        2. écrit la valeur dans le modèle au bon l'index: model.setData(...)

        https://doc.qt.io/qt-5/model-view-programming.html#submitting-data-to-the-model

        Mémo: editor.value() -> model.setDdata()
        """
        editor.interpretText()
        value = editor.value()
        model.setData(index, value, Qt.EditRole)


    def updateEditorGeometry(self, editor, option, index):
        """
        It is the responsibility of the delegate to manage the editor's geometry.
        The geometry must be set when the editor is created, and when the item's size or position in the view is changed.
        Fortunately, the view provides all the necessary geometry information inside a view option object.
 
        In this case, we just use the geometry information provided by the view option in the item rectangle.
        A delegate that renders items with several elements would not use the item rectangle directly.
        It would position the editor in relation to the other elements in the item.

        https://doc.qt.io/qt-5/model-view-programming.html#updating-the-editor-s-geometry
        """
        editor.setGeometry(option.rect)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    table_view = QTableView()
    my_model = MyModel()
    table_view.setModel(my_model)

    delegate = MyDelegate()
    table_view.setItemDelegate(delegate)

    table_view.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
