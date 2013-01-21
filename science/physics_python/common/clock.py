# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import time

class RealtimeClock:
    
    delta_time = None
    time = None

    _former_time = None
    _init_time = None

    def __init__(self):
        self._init_time = time.time()
        self._former_time = self._init_time
        self.time = 0

    def update(self):
        "Update the clock (add elapsed time since the last call)"
        current_time = time.time()
        self.delta_time = current_time - self._former_time
        self.time = current_time - self._init_time
        self._former_time = current_time


class SimulationtimeClock:

    delta_time = None
    time = None

    def __init__(self, delta_time):
        self.delta_time = delta_time
        self.time = 0

    def update(self):
        "Update the clock (add delta_time value)"
        self.time += self.delta_time

