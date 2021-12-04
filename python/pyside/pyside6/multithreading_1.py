#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Src: https://www.pythonguis.com/tutorials/multithreading-pyside6-applications-qthreadpool/

from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget, QMainWindow, QApplication
from PySide6.QtCore import QTimer, QRunnable, Slot, Signal, QObject, QThreadPool

import sys
import time
import traceback


class WorkerSignals(QObject):
    error = Signal(tuple)


class Worker(QRunnable):
    def __init__(self):
        super(Worker, self).__init__()
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            for t in range(10):
                print(t)
                time.sleep(1)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        btn = QPushButton("Run")
        btn.pressed.connect(self.btn_callback)
        self.setCentralWidget(btn)
        self.show()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum {} threads".format(self.threadpool.maxThreadCount()))


    def btn_callback(self):
        worker = Worker()
        self.threadpool.start(worker)


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()