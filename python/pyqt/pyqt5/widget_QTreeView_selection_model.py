#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref:
# - http://doc.qt.io/qt-5/modelview.html
# - http://doc.qt.io/qt-5/qabstractitemview.html#selectionChanged
# - http://doc.qt.io/qt-5/qitemselection.html
# - http://doc.qt.io/qt-5/qmodelindex.html

import sys
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QTreeView


def get_path(item):
    seek_root = item
    path = str(seek_root.data(Qt.DisplayRole))

    while seek_root.parent() != QModelIndex():
        seek_root = seek_root.parent()
        path = str(seek_root.data(Qt.DisplayRole)) + " / " + path

    return path


def print_selection(new_selection, old_selection):
    old_selection_indexes = [index for index in old_selection.indexes()]
    new_selection_indexes = [index for index in new_selection.indexes()]

    if len(old_selection_indexes) > 0:
        old_path = get_path(old_selection_indexes[0])
    else:
        old_path = ""

    new_path = get_path(new_selection_indexes[0])

    print(old_path, " -> ", new_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    tree_view = QTreeView()

    ###

    model = QStandardItemModel(None)

    rootItem = model.invisibleRootItem()

    # Defining a couple of items
    americaItem = QStandardItem("America")
    canadaItem = QStandardItem("Canada")
    europeItem = QStandardItem("Europe")
    franceItem = QStandardItem("France")
    brittanyItem = QStandardItem("Brittany")

    # Building up the hierarchy
    rootItem.appendRow(americaItem)
    rootItem.appendRow(europeItem)
    americaItem.appendRow(canadaItem)
    europeItem.appendRow(franceItem)
    franceItem.appendRow(brittanyItem)

    tree_view.setModel(model)

    # Bind selection to the print_selection function (must be after the model setup)
    selection_model = tree_view.selectionModel()
    selection_model.selectionChanged.connect(print_selection)

    tree_view.expandAll()      # expand all (this is not the case by default)
    tree_view.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)