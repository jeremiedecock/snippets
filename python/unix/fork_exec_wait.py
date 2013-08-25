#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import sys
import os

CMD = 'sleep'

pid = os.fork()

if pid==0:
    # CHILD PROCESS
    try:
        os.execlp(CMD, CMD, '3')
    except OSError as e:
        print "ERROR: can't run", CMD
    sys.exit(1)

# PARENT PROCESS
print CMD, "(PID {})".format(pid)
(wait_pid, status) = os.wait()        # wait the child process
if os.WIFEXITED(status):
    print "{} EXITED: {}".format(wait_pid, os.WEXITSTATUS(status))
elif os.WIFSIGNALED(status):
    print "{} SIGNALED: {}".format(wait_pid, os.WTERMSIG(status))

