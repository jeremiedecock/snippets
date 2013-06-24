#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# See http://docs.python.org/2/library/multiprocessing.html
# To exchange objects between processes, use multiprocessing.Queues or
# multiprocessing.Pipes

import multiprocessing
import time
import os

def hello(lock, msg):
    for i in range(10):
        lock.acquire()
        print os.getpid(), msg
        lock.release()
        time.sleep(0.1)

def main():
    """Main function"""

    lock = multiprocessing.Lock()

    proc1 = multiprocessing.Process(target=hello, args=(lock, "hello"))
    proc2 = multiprocessing.Process(target=hello, args=(lock, "hi"))

    proc1.start()
    proc2.start()

    # The main process waits for its children
    proc1.join()
    proc2.join()
    print "exit"

if __name__ == '__main__':
    main()
