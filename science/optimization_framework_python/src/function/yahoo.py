# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

__all__ = ['YahooFunction']

import numpy as np
from matplotlib.finance import quotes_historical_yahoo
import datetime

import function

class YahooFunction(function.ObjectiveFunction):

    def __init__(self):
        self.ndim = 1

        date1 = datetime.date(1995, 1, 1) 
        date2 = datetime.date(2004, 4, 12)

        quotes = quotes_historical_yahoo('INTC', date1, date2)
        #self._quote = [q[1] for q in quotes]
        self._quote = [-q[1] for q in quotes]

        self.domain_min = 0. * np.ones(self.ndim)
        self.domain_max = len(self._quote) * np.ones(self.ndim)

    def _eval_one_sample(self, x):
        #y = float("-inf")
        y = float("inf")
        if self.domain_min <= x < self.domain_max:
            y = self._quote[int(x)]
        return y

