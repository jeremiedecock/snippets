#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# This snippet requires a Posix compliant operating system (eg. it doesn't
# works on Ms Windows).

import os
import sys

def main():
    """Main function"""

    pid = os.fork()
    if pid == -1:
        print >> sys.stderr, "Fork error"
        sys.exit(1)

    if pid == 0:
        # child process
        print "Hello from the child process ({0})".format(os.getpid())
    else:
        # parent process
        print "Hello form the parent process ({0})".format(os.getpid())
        os.wait()   # the parent process waits for the end of its child

if __name__ == '__main__':
    main()
