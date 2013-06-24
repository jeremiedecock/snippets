#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# See http://docs.python.org/2/library/multiprocessing.html

import multiprocessing
import time
import os

def hello(msg):
    for i in range(10):
        print os.getpid(), msg
        time.sleep(0.1)

def main():
    """Main function"""

    proc1 = multiprocessing.Process(target=hello, args=("hello",))
    proc2 = multiprocessing.Process(target=hello, args=("hi",))

    proc1.start()
    proc2.start()

    # The main process waits for its children
    proc1.join()
    proc2.join()
    print "exit"

if __name__ == '__main__':
    main()
