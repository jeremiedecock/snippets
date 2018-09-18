#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: https://stackoverflow.com/questions/28660287/sort-qtableview-in-pyqt5

import numpy as np
import pandas as pd
import sys

from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtWidgets import QApplication, QTableView

class PandasModel(QAbstractTableModel):

    def __init__(self, df, parent=None):
        super().__init__(parent)

        self._df = df

    def rowCount(self, parent):
        return self._df.values.shape[0]

    def columnCount(self, parent):
        return self._df.values.shape[1]

    def data(self, index, role):
        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole:
            return str(self._df.iloc[row, column])

        return None

    def headerData(self, index, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._df.columns[index]
            elif orientation == Qt.Vertical:
                return self._df.index[index]

        return None

#    def sort(self, column_index, order):
#        """Sort table by given column number."""
#        try:
#            self.layoutAboutToBeChanged.emit()
#            self._df = self._df.sort_values(self._df.columns[column_index], ascending=not order)
#            self.layoutChanged.emit()
#        except Exception as e:
#            print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    NUM_ROWS = 50
    NUM_COLUMNS = 10
    df = pd.DataFrame(np.random.randint(0, 100, size=[NUM_ROWS, NUM_COLUMNS]),
                      index=["row{}".format(index) for index in range(NUM_ROWS)],
                      columns=["col{}".format(index) for index in range(NUM_COLUMNS)])

    table_view = QTableView()
    my_model = PandasModel(df=df)
    table_view.setModel(my_model)
    table_view.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)
