#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# see: https://docs.python.org/3.3/library/subprocess.html#module-subprocess

import os
import sys
import subprocess

TIMEOUT=3  # seconds

# If you launch a sub-process (even with shell=False), then the
# subprocess.Popen.kill() function will only kill that sub-process (so if there
# are any "grandchild" processes, they won't be terminated.).
# See: http://stackoverflow.com/questions/3908063/python-subprocess-with-shell-true-redirections-and-platform-independent-subproc
#
# The solution is to use preexec_fn to cause the subprocess to acquire it's own
# session group (then a signal is sent to all processes in that session group).
# See: http://stackoverflow.com/questions/3876886/timeout-a-subprocess

def execute(args):
    try:
        output = subprocess.check_output(args, stderr=subprocess.STDOUT, universal_newlines=True, timeout=TIMEOUT)
        #output = subprocess.check_output(args, stderr=subprocess.STDOUT, universal_newlines=True, timeout=TIMEOUT, preexec_fn=os.setsid)
        print(output)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print("Execution failed:", e, file=sys.stderr)
        print("  Cmd:", e.cmd, file=sys.stderr)
        print("  Args:", e.args, file=sys.stderr)
        print("  Return code:", e.returncode, file=sys.stderr)
        print("  Output message:", e.output, file=sys.stderr)
    except subprocess.TimeoutExpired as e:
        print("Execution stopped:", e, file=sys.stderr)
        print("  Cmd:", e.cmd, file=sys.stderr)
        print("  Args:", e.args, file=sys.stderr)
        print("  Output message:", e.output, file=sys.stderr)
        print("  Timeout:", e.timeout, file=sys.stderr)

def main():
    """Main function"""

    # subprocess.check_output is a convenience functions (a wrapper).
    # For more advanced use cases, the underlying subprocess.Popen interface
    # can be used directly.

    # Test 1
    print("TEST1")
    execute(["ls", "."])
    print()

    # Test 2
    print("TEST2")
    execute(["ls", "unknown_file"])
    print()

    # Test 3
    print("TEST3")
    execute(["unknown_cmd"])
    print()

    # Test 4
    print("TEST4")
    execute(["sleep", "10"])


if __name__ == '__main__':
    main()
