#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import thread
import time

def hello(lock):
    lock.acquire_lock()                     # acquire a lock
    print "hello form ", thread.get_ident() # print the thread id
    lock.release_lock()                     # release the lock


def main():
    """Main function"""

    lock = thread.allocate_lock()

    thread1 = thread.start_new_thread(hello, (lock,))
    thread2 = thread.start_new_thread(hello, (lock,))
    thread3 = thread.start_new_thread(hello, (lock,))

    time.sleep(1)


if __name__ == '__main__':
    main()
