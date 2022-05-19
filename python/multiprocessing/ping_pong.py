#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# See http://docs.python.org/2/library/multiprocessing.html
# To exchange objects between processes, use multiprocessing.Queues or
# multiprocessing.Pipes

import multiprocessing
import time
import os

def proc1_func(lock):
    for i in range(10):
        lock.acquire()
        print(f"Ping ({os.getpid()})")
        lock.release()
        time.sleep(.1)

def proc2_func(lock):
    for i in range(10):
        lock.acquire()
        print(f"Pong ({os.getpid()})")
        lock.release()
        time.sleep(.1)

def main():
    """Main function"""

    lock = multiprocessing.Lock()

    proc1 = multiprocessing.Process(target=proc1_func, args=(lock, ))
    proc2 = multiprocessing.Process(target=proc2_func, args=(lock, ))

    proc1.start()
    proc2.start()

    # The main process waits for its children
    proc1.join()
    proc2.join()
    print("exit")

if __name__ == '__main__':
    main()
