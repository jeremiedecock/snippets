#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Src: https://www.pythonguis.com/tutorials/multithreading-pyside6-applications-qthreadpool/

from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget, QMainWindow, QApplication
from PySide6.QtCore import QTimer, QRunnable, Slot, Signal, QObject, QThreadPool

import sys
import time
import traceback


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    error
        tuple (exctype, value, traceback.format_exc() )

    progress
        int indicating % progress
    '''
    error = Signal(tuple)
    progress = Signal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    '''

    def __init__(self):
        super(Worker, self).__init__()
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            for n in range(0, 5):
                time.sleep(1)
                self.signals.progress.emit(n/4*100)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0
        self.label = QLabel("Start")

        btn = QPushButton("Run a new job")
        btn.pressed.connect(self.btn_callback)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum {} threads".format(self.threadpool.maxThreadCount()))

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timer_callback)
        self.timer.start()

    def btn_callback(self):
        # Pass the function to execute
        worker = Worker()
        worker.signals.progress.connect(self.progress_callback)

        # Execute
        self.threadpool.start(worker)

    def progress_callback(self, percent_progress):
        print(r"{}% done".format(percent_progress))

    def timer_callback(self):
        self.counter +=1
        self.label.setText("Counter: %d" % self.counter)


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()