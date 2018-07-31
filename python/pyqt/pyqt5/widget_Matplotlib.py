#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://pythonspot.com/en/pyqt5-matplotlib/

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QHBoxLayout

#import matplotlib
#matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import random


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        plot_canvas = PlotCanvas(self, width=5, height=4)

        # Set the layout
        layout = QHBoxLayout()
        layout.addWidget(plot_canvas)
        self.setLayout(layout)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # Plot
        data = [random.random() for i in range(25)]

        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')

        self.draw()


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
