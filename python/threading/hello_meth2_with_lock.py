#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# See:
# - http://docs.python.org/2/library/threading.html
# - http://www.tutorialspoint.com/python/python_multithreading.htm

import threading
import time

def foo(lock, iterations):
    for i in range(iterations):
        lock.acquire()
        print threading.currentThread().name,
        print threading.currentThread().ident,
        print threading.activeCount(),
        print threading.enumerate()
        lock.release()
        time.sleep(0.2)

def main():
    """Main function"""

    lock = threading.Lock()

    thread1 = threading.Thread(target=foo, args=(lock, 10))
    thread2 = threading.Thread(target=foo, args=(lock, 15))

    thread1.start()
    thread2.start()

    # Let the main thread do something too...
    for i in range(5):
        lock.acquire()
        print threading.currentThread().name,
        print threading.currentThread().ident,
        print threading.activeCount(),
        print threading.enumerate()
        lock.release()
        time.sleep(0.2)

    # Main thread waits for all threads to complete
    thread1.join()
    thread2.join()
    print "Exiting Main Thread"

if __name__ == '__main__':
    main()
