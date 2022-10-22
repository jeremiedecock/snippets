#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: https://doc.qt.io/qt-6/modelview.html#3-1-treeview
#      https://doc.qt.io/qt-6/qtreeview.html

import sys

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QTreeView

tag_lists = [
    ["A", "B", "C", "B", "D"],
    ["A", "B", "H", "A"],
    ["C", "B", "D"],
    ["C", "B", "D"],
    ["K"]
]

if __name__ == '__main__':
    app = QApplication(sys.argv)

    tree_view = QTreeView()

    ###

    model = QStandardItemModel(None)

    rootItem = model.invisibleRootItem()

    ###

    adjacency_set = set()

    for tag_list in tag_lists:
        if len(tag_list) > 0:
            adjacency_set.add((None, (tag_list[0],)))

            for child_tag_index in range(1, len(tag_list)):
                parent_tag_index = child_tag_index - 1
                parent_path_tuple = tuple(tag_list[:parent_tag_index + 1])
                child_path_tuple = tuple(tag_list[:child_tag_index + 1])
                adjacency_set.add((parent_path_tuple, child_path_tuple))

    for adjacency_couple in adjacency_set:
        print(f"{adjacency_couple[0]} -> {adjacency_couple[1]}")

    ###

    items_dict = {}

    # Defining a couple of items
    for adjacency_couple in adjacency_set:
        parent_path_tuple = adjacency_couple[0]
        child_path_tuple = adjacency_couple[1]

        if parent_path_tuple not in items_dict:
            if parent_path_tuple is None:
                items_dict[parent_path_tuple] = rootItem
            else:
                items_dict[parent_path_tuple] = QStandardItem(parent_path_tuple[-1])   # k[-1]    "/".join(k)

        if child_path_tuple not in items_dict:
            items_dict[child_path_tuple] = QStandardItem(child_path_tuple[-1])   # v[-1]     "/".join(v)

        items_dict[parent_path_tuple].appendRow(items_dict[child_path_tuple])

    tree_view.setModel(model)
    tree_view.expandAll()      # expand all (this is not the case by default)
    tree_view.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)