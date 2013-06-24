#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# See:
# - http://docs.python.org/2/library/threading.html
# - http://www.tutorialspoint.com/python/python_multithreading.htm

import threading
import time

def hello(msg):
    for i in range(10):
        print threading.currentThread().name, msg
        time.sleep(0.1)

def main():
    """Main function"""

    thread1 = threading.Thread(target=hello, args=("hello",))
    thread2 = threading.Thread(target=hello, args=("hi",))

    thread1.start()
    thread2.start()

if __name__ == '__main__':
    main()
