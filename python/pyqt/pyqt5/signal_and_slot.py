#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Src: https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html

from PyQt5.QtCore import QObject, pyqtSignal

class Foo(QObject):

    # Define a new signal that has no arguments.
    # New signals should only be defined in sub-classes of QObject.
    # They must be part of the class definition and cannot be dynamically added as class attributes after the class has been defined.
    sig_1 = pyqtSignal()

    # This defines a signal that takes two integer arguments.
    sig_2 = pyqtSignal(int, int)

    ## The following two lines don't work!
    #def __init__(self):
    #    self.sig_1 = pyqtSignal()


    def slot_1(self):
        print("Sig_1 signal received")

    def slot_2(self, n1, n2):
        print("Sig_2 signal received", n1, n2)


    def connect_sig_1(self):
        # Connect the sig_1 signal to slot_1
        self.sig_1.connect(self.slot_1)

    def disconnect_sig_1(self):
        # Disonnect the sig_1 signal from slot_1
        self.sig_1.disconnect(self.slot_1)    # disconnect([slot])

    def emit_sig_1(self):
        # Emit the signal.
        self.sig_1.emit()


foo = Foo()

foo.connect_sig_1()
foo.emit_sig_1()
foo.disconnect_sig_1()
foo.emit_sig_1()

print("-" * 10)

foo.sig_1.connect(foo.slot_1)
foo.sig_1.emit()
foo.sig_1.disconnect(foo.slot_1)

print("-" * 10)

foo.sig_2.connect(foo.slot_2)
foo.sig_2.emit(1, 2)
foo.sig_2.disconnect(foo.slot_2)
