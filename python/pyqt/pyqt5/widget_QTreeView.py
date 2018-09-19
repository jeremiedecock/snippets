#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: http://doc.qt.io/qt-5/modelview.html#2-1-a-read-only-table

import sys
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QTreeView


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
    tree_view.expandAll()      # expand all (this is not the case by default)
    tree_view.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)