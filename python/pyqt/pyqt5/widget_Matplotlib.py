#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QHBoxLayout

#import matplotlib
#matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
import pandas as pd


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(600, 500)

        plot_canvas = PlotCanvas(self, width=5, height=4, dpi=100)

        # Set the layout
        layout = QHBoxLayout()
        layout.addWidget(plot_canvas)
        self.setLayout(layout)


class PlotCanvas(FigureCanvas):
    """This is a Matplotlib QWidget.

    See https://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.data_x = np.arange(0, 10, 0.1)
        self.data_y = np.sin(self.data_x)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        s = pd.DataFrame(self.data_y, index=self.data_x)
        s.plot(ax=self.axes)

        #self.axes.plot(x, y)

#    def update_figure(self):
#        self.axes.cla()
#
#        s = pd.DataFrame(self.data_y, index=self.data_x)
#        s.plot(ax=self.axes)
#        #self.axes.plot(x, y)
#
#        self.draw()


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
