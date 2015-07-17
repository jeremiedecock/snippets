#!/usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.finance import quotes_historical_yahoo_ohlc
import datetime

date1 = datetime.date( 1995, 1, 1 ) 
date2 = datetime.date( 2004, 4, 12 )
quotes = quotes_historical_yahoo_ohlc('INTC', date1, date2)

opens = [q[1] for q in quotes]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(opens)

# SAVE FILES ######################
plt.savefig("finance_yahoo_dataset.png")

plt.show()
