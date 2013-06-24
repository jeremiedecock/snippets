#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# See:
# - http://docs.python.org/2/library/threading.html
# - http://www.tutorialspoint.com/python/python_multithreading.htm

import threading
import time

class Foo(threading.Thread):
    def __init__(self, lock, iterations):
        threading.Thread.__init__(self)
        self._lock = lock
        self._iterations = iterations

    def run(self):
        for i in range(self._iterations):
            self._lock.acquire()
            print self.name,
            print self.ident,
            print threading.activeCount(),
            print threading.enumerate()
            self._lock.release()
            time.sleep(0.2)

def main():
    """Main function"""

    lock = threading.Lock()

    thread1 = Foo(lock, iterations=10)
    thread2 = Foo(lock, iterations=15)

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
