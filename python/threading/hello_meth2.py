#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# See:
# - http://docs.python.org/2/library/threading.html
# - http://www.tutorialspoint.com/python/python_multithreading.htm

import threading
import time

def foo(iterations):
    for i in range(iterations):
        print threading.currentThread().name,
        print threading.currentThread().ident,
        print threading.activeCount(),
        print threading.enumerate()
        time.sleep(0.2)

def main():
    """Main function"""

    thread1 = threading.Thread(target=foo, args=(10,))
    thread2 = threading.Thread(target=foo, args=(15,))

    thread1.start()
    thread2.start()

    # Let the main thread do something too...
    for i in range(5):
        print threading.currentThread().name
        time.sleep(0.2)

    # Main thread waits for all threads to complete
    thread1.join()
    thread2.join()
    print "Exiting Main Thread"

if __name__ == '__main__':
    main()
